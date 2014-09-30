from django.core.management import BaseCommand
from django.core import management
from django.utils.six.moves import input
from colorama import Fore, Back, Style, init
from django.contrib.sites.models import Site
from django.db import transaction
import getpass

# FIXME: This should also fill out database details, client URI details, etc
class Command(BaseCommand):
  help = 'Installs Spiff'

  def handle(self, *args, **options):
    init()
    print Style.BRIGHT+"Greetings, Hacker! You are about to install"
    print Fore.YELLOW+"""  ____                                             
 / ___| _ __   __ _  ___ ___ _ __ ___   __ _ _ __  
 \___ \| '_ \ / _` |/ __/ _ \ '_ ` _ \ / _` | '_ \ 
  ___) | |_) | (_| | (_|  __/ | | | | | (_| | | | |
 |____/| .__/_\__,_|\___\___|_| |_| |_|\__,_|_| |_|
       |_/ ___| _ __ (_)/ _|/ _|                   
         \___ \| '_ \| | |_| |_                    
          ___) | |_) | |  _|  _|                   
         |____/| .__/|_|_| |_|                     
               |_|""" + Style.RESET_ALL
    print ("In order to customize your installation, I (a simplistic AI) will "
           "be asking you a series of questions.")
    print ("First, a few questions about your hacker space.")
    print ("At various places within Spiff, your space's name will be needed. "
           "It should be able to fill in the blank:")
    print Fore.GREEN+'"Welcome to _______!"'+Fore.RESET
    while True:
      space_name = input("So, what is your hacker space's name? ")
      confirm = input(('So you mean to say '+Style.BRIGHT+'"Welcome to %s, fellow hacker!"?'+Style.NORMAL+' [Y/n] ')%(space_name))
      if confirm.lower() == "y" or confirm == "":
        break
    print Style.BRIGHT+'Excellent!!!'+Style.NORMAL
    print "Certain machine-readable things will need to know your space's canonical domain name."
    print "For example, Noisebridge's is '"+Fore.GREEN+"noisebridge.net"+Fore.RESET+"'"
    while True:
      space_domain = input("So, what is the canonical domain name for your hacker space? ")
      confirm = input(('So I could ping "'+Style.BRIGHT+'%s'+Style.NORMAL+'", right? [Y/n] ')%(space_domain))
      if confirm.lower() == "y" or confirm == "":
        break
    print Style.BRIGHT+'Excellent!!!'+Style.NORMAL
    site = Site(domain=space_domain, name=space_name)

    print ("Now, we'll want to set up an admin user. This person has complete "
           "access to everything and is magically given every permission "
           "without question.")
    print "More superusers can be created later via the createsuperuser command"
    username = input("Username: ")
    email = input("E-mail: ")
    password = None
    while password is None:
      password = getpass.getpass()
      password2 = getpass.getpass('Password (again): ')
      if password != password2:
        print "Error: Your passwords didn't match."
        password = None
        continue

    print "Okay, here's what I've gathered about your hacker space."
    print "Hackerspace name: "+Style.BRIGHT+site.name+Style.NORMAL
    print "Hackerspace domain: "+Style.BRIGHT+site.domain+Style.NORMAL
    print "Admin username: "+Style.BRIGHT+username+Style.NORMAL
    print "Admin email: "+Style.BRIGHT+email+Style.NORMAL
    print "Admin password: "+Style.BRIGHT+"hunter2"+Style.NORMAL

    confirm = input("Does all of this look okay to you? [Y/n] ")
    if confirm.lower() == "y" or confirm == "":
      print Fore.GREEN+"Installing to database..."+Fore.RESET
      with transaction.atomic():
        site.save()
        User.objects.create_superuser({'username': username, 'password': password, 'email': email})
      print Style.YELLOW+Style.BRIGHT+"EXCELLENT!"+Style.NORMAL+Fore.RESET
      print Style.BRIGHT+"Your installation of Spiff is complete. Stay excellent, fellow hacker."+Style.NORMAL
    else:
      print Fore.RED+"Configuration abandoned."+Fore.RESET
