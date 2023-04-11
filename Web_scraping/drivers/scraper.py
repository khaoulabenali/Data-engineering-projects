from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

DRIVER_PATH = 'C:/Users/Data Science/Desktop/data engineering/freelance/recipe_scraping/chromedriver_win32/chromedriver.exe'
options = Options()
options.add_experimental_option('excludeSwitches', ['load-extension', 'enable-automation'])
#options.headless = True
options.add_argument("--window-size=1920,1200")
options.add_argument("--disable-notifications")
prefs = {"credentials_enable_service": False,
                "profile.password_manager_enabled": False}
options.add_experimental_option("prefs", prefs)
data_init = {'name': [], 'category': [],'author':[],'prep_time':[],'cook_time':[],'total_prep_time':[],'description':[],'calories':[], 'calories_unit':[],'image':[],'recipe_ingredients':[],'recipe_instructions':[]}



class Scraper:
    def __init__(self):
        self._driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
        self._data = pd.DataFrame.from_dict(data_init)

    def scroll_recipes(self):
        recipes_links = []
        nb_recipes = None
        try:
            self._driver.find_element(By.XPATH,'//*[@id="cookie_action_close_header"]').click()
        except:
            pass
        while True:
            try:
                self._driver.find_element(By.XPATH,'//*[@id="post-9174"]/div/div/div[7]/div/div/div/div[3]/a/span[1]/span').click()
                time.sleep(4)
                    
            except :
                print("done scrolling")
                break
        try :
            nb_recipes = len(self._driver.find_elements(By.XPATH,'//*[@id="post-9174"]/div/div/div[7]/div/div/div/div[1]/article'))
            recipes_links = [ self._driver.find_element(By.XPATH, '//*[@id="post-9174"]/div/div/div[7]/div/div/div/div[1]/article['+str(i)+']/div/a').get_attribute("href") for i in range(1,nb_recipes+1)]
            return(nb_recipes,recipes_links)
        except Exception as e:
            print(e)
            return(nb_recipes,recipes_links)

    def get_recipe_info(self,recipe_link):
        self._driver.get(recipe_link)
        try :
            name = self._driver.find_element(By.XPATH, '//*[@class="entry-title"]').text
        except Exception as e:
            name = ""
            print("Couldn't scrape name")
            pass
        try:
            category = self._driver.find_element(By.XPATH, '//*[@class="ast-terms-link"]/a').text
        except Exception as e:
            category=""
            print("Couldn't scrape category")
            pass
        try:
            author = self._driver.find_element(By.XPATH, '//*[@class="author-name"]').text
        except Exception as e:
            author=""
            print("Couldn't scrape author")
            pass
        try:
            description = self._driver.find_element(By.XPATH, '//*[@class="elementor-widget-container"]/p').text
        except Exception as e:
            description=""
            print("Couldn't scrape description")
            pass
        try:
            calories = self._driver.find_element(By.XPATH, '//*[@class="wprm-recipe-nutrition-with-unit"]/span[1]').text
            calories_unit = self._driver.find_element(By.XPATH, '//*[@class="wprm-recipe-nutrition-with-unit"]/span[2]').text
        except Exception as e:
            calories=""
            calories_unit=""
            print("Couldn't scrape calories")
            pass
        try:
            image = self._driver.find_element(By.XPATH, '//*[@class="entry-header "]/div/img').get_attribute("src")
        except Exception as e:
            image=""
            print("Couldn't scrape image")
            pass
        try:
            prep_time = self._driver.find_element(By.XPATH, '//*[@class="wprm-recipe wprm-recipe-template-saeo"]/div[3]/div[1]/span[2]').text
        except Exception as e:
            prep_time=""
            print("Couldn't scrape prep_time")
            pass
        try:
            cook_time = self._driver.find_element(By.XPATH, '//*[@class="wprm-recipe wprm-recipe-template-saeo"]/div[3]/div[2]/span[2]').text
        except Exception as e:
            cook_time=""
            print("Couldn't scrape cook_time")
            pass
        try:
            total_prep_time = self._driver.find_element(By.XPATH, '//*[@class="wprm-recipe wprm-recipe-template-saeo"]/div[3]/div[3]/span[2]').text
        except Exception as e:
            total_prep_time=""
            print("Couldn't scrape total_prep_time")
            pass
        try:
            ingredients_components = [component.text for component in self._driver.find_elements(By.XPATH, '//*[@class="wprm-recipe-ingredient-group"]/h4')]
            ingredients = [ingredient.text for ingredient in self._driver.find_elements(By.XPATH, '//*[@class="wprm-recipe-ingredients"]')]
            if ingredients_components:
                recipe_ingredients = [{ingredients_components[i]:ingredients[i]} for i in range(len(ingredients_components))]
            else:
                recipe_ingredients=ingredients
        except Exception as e:
            recipe_ingredients=[]
            print("Couldn't scrape recipe_ingredients")
            pass
        try:
            instructions_components = [component.text for component in self._driver.find_elements(By.XPATH, '//*[@class="wprm-recipe-instruction-group"]/h4')]
            instructions = [ingredient.text for ingredient in self._driver.find_elements(By.XPATH, '//*[@class="wprm-recipe-instructions"]')]
            if instructions_components:
                recipe_instructions = [{instructions_components[i]:instructions[i]} for i in range(len(instructions_components))]
            else:
                recipe_instructions=instructions 
        except Exception as e:
            recipe_instructions=[]
            print("Couldn't scrape recipe_instructions")
            pass
        result = {"name":name,"link":recipe_link,"category":category,"author":author,"prep_time":prep_time,"cook_time":cook_time,"total_prep_time":total_prep_time,"description":description,"calories":calories,"calories_unit":calories_unit,"image":image,"recipe_ingredients":recipe_ingredients,"recipe_instructions":recipe_instructions}
        return(result) 
    
    def store_recipe(self,recipe_info,storing_file):
        try:
            self._data = self._data.append(recipe_info, ignore_index=True)
            self._data.to_excel(storing_file)
            print(recipe_info["link"]+" ::::: Successfully saved!!")
        except Exception as e:
            print(e)

    def scrape_recipes(self,blog_url,storing_file):
        try :
            self._driver.get(blog_url)
            nb_recipes,recipes_links = self.scroll_recipes()
            print(" This blog is composed of "+str(nb_recipes)+" recipe.")
            for recipe_link in recipes_links:
                recipe_info = self.get_recipe_info(recipe_link)
                self.store_recipe(recipe_info,storing_file)
            self._driver.quit()
        except Exception as e:
            print(e)
            self._driver.quit()
      
        
