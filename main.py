# -*- coding: utf-8 -*-
import os
import sys
sys.excepthook = sys.__excepthook__
from random import randrange
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver
from time import sleep
import credentials
# from secrets import pw

class Insta:
    def __init__(self,user,pw):
        self.user = user
        self.actionChains = ActionChains
        self.firefox = webdriver.Firefox()
        
        self.firefox.get('https://www.instagram.com/accounts/login/')
        sleep(1)

        # Logando
        # main.py:20: DeprecationWarning: find_element_by_xpath is deprecated. Please use find_element(by=By.XPATH, value=xpath) instead
        self.firefox.find_element(By.XPATH, "//input[@name=\"username\"]").send_keys(user)
        self.firefox.find_element(By.XPATH, "//input[@name=\"password\"]").send_keys(pw)
        self.firefox.find_element(By.XPATH, '//button[@type="submit"]').click()
        sleep(8)
        self.firefox.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]").click()
        # sleep(2)
        # self.firefox.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()

    def get_followers(self):
        # 'moda_fashion79','mulhermodaintima_'
        users = ['moda_fashion79','roupas.em.atacado']
        number_to_follow = 200
        for item in users:
            self.firefox.get('https://www.instagram.com/'+ item)
            sleep(5)
            self.firefox.find_element(By.XPATH, "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a").click()
            sleep(2)
            
            scroll_box = self.firefox.find_element(By.XPATH, "/html/body/div[5]/div/div/div[2]")
            totalScroll = 0
            qtdScroll =10
            last_ht, ht = 0, 1

            while last_ht != ht:
                # follow = scroll_box.find_elements_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div/li[13]/div/div[2]/button")
                follow = scroll_box.find_elements_by_xpath("//button[contains(text(), 'Follow') and @class='sqdOP  L3NKy   y3zKF     ']")
                i = 1
                for follower in follow:
                    if(i != 1):
                        self.firefox.execute_script("arguments[0].click();", follower)
                        sleep(2)
                    i+=1
                sleep(2)

                last_ht = ht
                sleep(1)
                ht = self.firefox.execute_script("""
                    arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                    return arguments[0].scrollHeight;
                    """, scroll_box)
            
            self.firefox.find_element(By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[2]/button").click() # fechando janela          


    def folloOneByOne(self,usersInput,qtdLimiteScroll=0):
        users = usersInput.split(',')
        
        for item in users:
            self.firefox.get('https://www.instagram.com/'+ item)
            sleep(3)
            
            # buttonFollowers = self.firefox.find_element(By.XPATH, "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a")
            # sleep(1)
            # buttonFollowers.click()
            # sleep(3)
            
            # Wait for initialize, in seconds

            buttonFollowers = self.firefox.find_element(By.XPATH, "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/div")
            self.firefox.implicitly_wait(10)
            ActionChains(self.firefox).move_to_element(buttonFollowers).click(buttonFollowers).perform()
            sleep(3)

            scroll_box = self.firefox.find_element(By.XPATH, "/html/body/div[6]/div/div/div/div[2]")
            totalScroll = qtdLimiteScroll
            qtdScroll=0
            print("---------------------------PEGANDO OS SEGUIDORES DO "+item+"-----------------------------------------")
            last_ht, ht = 0, 1
            while last_ht != ht:
                print(f"if {last_ht} != {ht}")
                qtdScroll = qtdScroll + 1
                last_ht = ht
                print(f"qtdScroll: {qtdScroll}. Totalscroll: {totalScroll}")
                sleep(1)
                ht = self.firefox.execute_script("""
                    arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                    return arguments[0].scrollHeight;
                    """, scroll_box)
                if(totalScroll > 0):
                    if(qtdScroll == totalScroll):
                        last_ht = 0
                        ht = 0
                
            divUsers = scroll_box.find_elements(By.XPATH, '/html/body/div[6]/div/div/div/div[2]/ul/div/li')
            # userToFollow = [follow.find_element_by_xpath for follow in divUsers if follow.find_element_by_xpath("//button[contains(text(), 'Follow') and @class='sqdOP  L3NKy   y3zKF     ']")]
            
            print("Analisamos ")
            print(len(divUsers))
            print("perfis")
            print("\n")
            
            usersToFollow =[]
            countListUsers = 0
            countDivUsers = 0
            penultimaPessoaDaLista = (len(divUsers) - 1)
            print("Separando apenas os FOLLOW. \nEssa operação pode levar alguns minutos...")
            for item in divUsers:
                countDivUsers +=1
                if(penultimaPessoaDaLista == countDivUsers):
                    break

                arText = item.text.split("\n")
                if (len(arText)):
                    if arText[len(arText)-1] == 'Follow':
                        usersToFollow.append(arText[0])
                        countListUsers +=1
                        print(str(countListUsers)+': '+arText[0])

            print(len(usersToFollow))
            print(" Novos usuarios")
            print("\n\n")
            print(usersToFollow)

            # follow = scroll_box.find_elements_by_xpath("//button[contains(text(), 'Follow') and @class='sqdOP  L3NKy   y3zKF     ']")
            # links = scroll_box.find_elements_by_tag_name('a')
            # names = [name.text for name in links if name.text != '']
               
            # print(names)
            self.firefox.find_element(By.XPATH, "/html/body/div[6]/div/div/div/div[1]/div/div[3]/div/button/div").click() # fechando janela
            
            # arrumar essa parte
            # entrando no meu perfil para comparar as pessoas que eu já sigo, porém já resolvi esse problema em cima.
            # print("---------------------------PEGANDO AS PESSOAS QUE EU ESTOU SEGUINDO-----------------------------------------")
            # following = self.getMyFollowers()
            # print (following)
            # print("---------------------------PEGANDO OS SEGUIDORES DO "+item+" QUE EU NAO ESTOU SEGUINDO-----------------------------------------")
            # not_following = [user for user in names if user not in following]
            # print(not_following)

            # for u in names:
            # for u in not_following:
            totalPessoasSeguidas = 0
            for u in usersToFollow:
                # if(u != "detroitmetal1"):continue
                totalPessoasSeguidas +=1
                print(totalPessoasSeguidas)
                self.firefox.get('https://www.instagram.com/'+ u)
                sleep(1)
                sleep(randrange(2))

                # toFollow = self.firefox.find_element(By.XPATH, "//button[contains(text(), 'Follow')]")
                
                toFollow = []
                toFollowOpDois = []
                toFollow = self.firefox.find_elements(By.XPATH, "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button/div")
                # toFollowOpDois = self.firefox.find_elements(By.XPATH, "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button")
                
                if(len(toFollow) > 0 and toFollow[0].text == 'Follow'):
                    toFollow[0].click()
                    sleep(2)
                else:
                    if(len(toFollowOpDois) > 0 and toFollowOpDois[0].text == 'Follow'):
                        toFollowOpDois[0].click()
                        sleep(2)


                if(len(self.firefox.find_elements(By.XPATH, "//*[contains(text(), 'This Account is Private')]")) > 0): continue
                
                # Assistindo stories
                # stories = self.firefox.find_element(By.XPATH, "/html/body/div[1]/section/main/div/div[1]/div/div/div/ul/li[3]/div/div/div[1]/div/img")
                sleep(1)
                stories = self.firefox.find_elements(By.XPATH, "/html/body/div[1]/section/main/div/header/div/div")
                if(len(stories) > 0):
                    stories[0].click()
                    #clicando no próximo 
                    sleep(2)
                    continueStore = True
                    while continueStore:
                        # proximoStorie = self.firefox.find_element(By.XPATH, "/html/body/div[1]/section/div[1]/div/section/div/button/div")
                        proximoStorie = self.firefox.find_elements(By.CLASS_NAME, "coreSpriteRightChevron")
                        if(len(proximoStorie)>0):
                            proximoStorie[0].click()
                            sleep(2)
                        else:
                            continueStore = False

                # Fim Assistindo stories
                
                abrirFotoOpacaoUm = []
                abrirFotoOpacaoDois = []
                abrirFotoOpacaoTres = []
                
                abrirFotoOpacaoUm = self.firefox.find_elements(By.XPATH, "/html/body/div[1]/section/main/div/div[2]/article/div/div/div[1]/div[1]")
                # if(len(abrirFotoOpacaoUm) <= 0 and len(abrirFotoOpacaoDois) <= 0 and len(abrirFotoOpacaoTres) <= 0): continue
                
                if(len(abrirFotoOpacaoUm)):
                    abrirFotoOpacaoUm[0].click()
                else:
                    abrirFotoOpacaoDois = self.firefox.find_elements(By.XPATH, "/html/body/div[1]/section/main/div/div[3]/article/div/div/div[1]/div[1]")
                    if(len(abrirFotoOpacaoDois)):
                        abrirFotoOpacaoDois[0].click()
                    else:
                        abrirFotoOpacaoTres = self.firefox.find_elements(By.XPATH, "/html/body/div[1]/section/main/div/div[4]/article/div[1]/div/div[1]/div[1]")
                        if(len(abrirFotoOpacaoTres)):
                            abrirFotoOpacaoTres[0].click()

                sleep(1.2)
                # /html/body/div[6]/div[3]/div/article/div/div[1]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/div[1]/img                
                foto = self.firefox.find_elements(By.XPATH, "/html/body/div[6]/div[3]/div/article/div/div[1]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div")
                if(len(foto) <= 0): continue
                
                actionChains = self.actionChains(self.firefox)
                actionChains.double_click(foto[0]).perform()
                
        

    def get_unfollowers(self,downloadFile=True):
        pathToSave = 'unfollowersList/unfollowersList'+self.user
        pathProgram = (os.path.dirname(os.path.abspath(__file__)))
        pathProgramFile = pathProgram+'/'+pathToSave+'.txt'
        self.firefox.get('https://www.instagram.com/'+ self.user)
        
        followers = self.getMyFollowers()
        following = self.getFollowing()

        not_following_back = [user for user in following if user not in followers]
        
        # if(downloadFile):
        with open(pathToSave+'.txt', 'w') as f:
            for item in not_following_back:
                f.write("%s\n" % item)
        
        print("\nsalvamos seu arquivo na pasta do projeto com o nome: unfollowersList"+self.user+".txt")
        # os.startfile(pathProgram)
        os.system('xdg-open "%s"' % pathProgramFile)
        return not_following_back
        # print(following)

    def stopFollowingUsersWhoDontFollowMe(self,excecoes):
        userExcecoes = excecoes.split(',')
        users = self.get_unfollowers(False)
        if(len(userExcecoes)>0):
            users = [user for user in users if user not in userExcecoes]
        i = 0
        for user in users:
            i +=1
            print()
            print(f"{i} de {len(users)}")
            self.firefox.get('https://www.instagram.com/'+ user)
            sleep(1)
            sleep(randrange(10))
            
            buttonUnFollow = self.firefox.find_elements(By.XPATH, "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/button")
            buttonUnFollowOpDois = self.firefox.find_elements(By.XPATH, "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button")
            
            if(len(buttonUnFollow)):
                buttonUnFollow[0].click()
            if(len(buttonUnFollowOpDois)):
                buttonUnFollowOpDois[0].click()
            
            sleep(1)
            sleep(randrange(3))
            self.firefox.find_element(By.XPATH, "//button[contains(text(),'Unfollow')]").click()
            sleep(1)
            sleep(randrange(10))
            

    def getMyFollowers(self):
        self.firefox.find_element(By.XPATH, "//a[contains(@href,'/followers')]").click()
        sleep(1)

        scroll_box = self.firefox.find_element(By.XPATH, "/html/body/div[6]/div/div/div[2]")
        
    
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.firefox.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)

        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.firefox.find_element(By.XPATH, "/html/body/div[6]/div/div/div[1]/div/div[2]/button")\
            .click()
        return names

    def getFollowing(self):
        self.firefox.find_element(By.XPATH, "//a[contains(@href,'/following')]").click()
        sleep(1)

        scroll_box = self.firefox.find_element(By.XPATH, "/html/body/div[6]/div/div/div[3]")
        
    
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.firefox.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)

        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.firefox.find_element(By.XPATH, "/html/body/div[6]/div/div/div[1]/div/div[2]/button")\
            .click()
        return names

print ("""
****************************Escolha uma opção****************************\n
1 Follow fast
2 Follow and like the last photo
3 list user don't follow you back
4 Stop following who doesn't follow you back
5 Stop following those who don't follow you back with exceptions
6 Close
\n************************************************************************\n
""")

menu=input("O que você gostaria de fazer? ")
usuario=input("qual é o seu usuario do instagram? ")
senha=input("qual eh a sua senha do instagram? ")

usuarioInformado = usuario if usuario != '' else credentials.USER
senhaInformada = senha if senha != '' else credentials.SECRET_PASS

print (menu)

if menu=="1":
    print("\n Seguir pessoas de forma rápida")
    bot = Insta(usuarioInformado,senhaInformada)
    bot.get_followers()
elif menu=="2":
    print("\n Seguir e curtir a última foto") 
    usersInput =input("Pegar os usuários de qual perfil?: \n")
    limiteScroll=int(input("Voce quer fazer quantos scrolls na lista de usuarios? 0 para ilimitado "))
    usersLimiteScroll = limiteScroll if limiteScroll != '' else 0
    usersInputToGet = usersInput if usersInput != '' else "rocketseat_oficial"
    bot = Insta(usuarioInformado, senhaInformada)
    bot.folloOneByOne(usersInputToGet, usersLimiteScroll)
elif menu=="3":
    print("\n Ver lista de quem nao te segue te volta") 
    bot = Insta(usuarioInformado,senhaInformada)
    bot.get_unfollowers()
elif menu=="4":
    print("\n Parar de seguir quem nao te segue de volta\n")
    bot = Insta(usuarioInformado,senhaInformada)
    bot.stopFollowingUsersWhoDontFollowMe('')
elif menu=="5":
    print("\n Parar de seguir quem nao te segue de volta\n")
    excecoes=input("Excecoes de usuarios separado por virgula ex: user1,user2,user3,user4: ")
    bot = Insta(usuarioInformado,senhaInformada)
    bot.stopFollowingUsersWhoDontFollowMe(excecoes)
    
    # bot.stopFollowingUsersWhoDontFollowMe()
elif menu=="6":
    print("\n Goodbye") 
elif menu !="":
    print("\n Not Valid Choice Try again") 



