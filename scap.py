"""
this app tracks Amazon prices

@author: Reza_Behzadfard
"""

from selenium import webdriver
import smtplib # this module help us to sending mail
import time

def check_price(URL):
    # enter your chromedriver address in your system
    driver = webdriver.Chrome("/home/oem/python-project/amazon-price-tracker/chromedriver")
    driver.get(URL)

    # get page information
    price = driver.find_element_by_xpath('.//*[@id="price_inside_buybox"]').text

    # delete dollor sign and . between numbers
    converted_price = price[1:].replace('.', '').strip()

    return converted_price

def send_mail(user_gmail, gmail_pwd, to_gmail, URL):
    Subject = "Product price fell down"
    Text = "Hey check this amazon link: price of your favorite goods fell down"
    Text = f"Hey check this amazon link: {URL}"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(user_gmail, gmail_pwd)
    Body = '\r\n'.join(['To: %s' % to_gmail, 'From: %s' % user_gmail, 'Subject: %s' % Subject,
                        '', Text])
    server.sendmail(user_gmail, [to_gmail], Body)
    print("email sent")

def main():
    # url of product
    URL = "https://www.amazon.com/Seagate-Portable-External-Hard-Drive/dp/B07CRG94G3/ref=lp_16225007011_1_2"
    
    # fill these three variable and enable less secure app of {user_gmail} to access gmail account
    user_gmail = "GMAIL_ADDRESS"
    gmail_pwd = "GMAIL_PWD"
    to_gmail = "GMAIL_ADDRESS"
    
    while True:
        price = int(check_price(URL))

        # send email if the real price is less than the specified price
        less_than_this_price = "PRICE"
        less_than_this_price = int(less_than_this_price.replace('.', ""))
        if price < less_than_this_price:
            send_mail(user_gmail, gmail_pwd, to_gmail, URL)

        # check price once a day
        time.sleep(86400)
        
if __name__ == '__main__': main()
