from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
from time_keeper import count


#driver.maximize_window()

#####################
def product_information(name):
    driver = webdriver.PhantomJS()#Chrome("C:/Users/Yash/Downloads/chromedriver_win32/chromedriver")
    driver.maximize_window()
    driver.get("https://www.midlandsci.com/")
    sleep(2)
    page_counter=4
    search = driver.find_element_by_css_selector("#SearchBox")
    search.send_keys(name)

    button = driver.find_element_by_css_selector("#btn_search")
    button.click()

    sleep(1)
    url = driver.current_url
    print(url)
    fullname = {"Ricca":"RiccaChemical", "Globe":"GlobeScientific", "Brandtech": "BrandtechScientific", "MTC Bio":"MTCBio"}
    try:
        driver.find_element_by_css_selector("#linkAttributeValueSupplier_{}".format(fullname[name])).click()
    except:
        driver.find_element_by_css_selector("#linkAttributeValueSupplier_{}".format(name)).click()
        
        
    pages = driver.find_element_by_css_selector(".ItemSearchResults_SummaryMessage").text
    pages = pages.split("of")
    total = pages[-1].split(".")
    total = int(total[0])
    #total = 5
    
    
    pt = pages[0].split("-")
    pt_st = pt[0].split(":")
    page_start, page_total = int(pt_st[1]), int(pt[1])
    sleep(1)
    #page_total=5
    
    #driver.execute_script("window.history.go(-1)")
    #driver.execute_script("window.scrollTo(0, 450)")
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.END)
    prd_price ={}
    prd_img={}
    prd_desp={}
    prd_mod={}
    sleep(5)
    total_ids=[]
    while True:
        for i in range(0, (page_total-page_start)+1):
            prd_id = driver.find_element_by_css_selector("#BaseList_TR_ResultLine_{}\ item_tr_customstyle > td:nth-child(1) > a:nth-child(2)".format(str(i))).text
            prd_desp[prd_id] = {}
            wait = True
            while wait:
                if prc != "WAIT":
                    prd_price[prd_id]
                    break
                else:
                    prc = driver.find_element_by_css_selector("#BaseList_TR_ResultLine_{}\ item_tr_customstyle > td:nth-child(3) > span:nth-child(1)".format(str(i))).text
                
                
            print("Got the Price")
            img = driver.find_element_by_css_selector("#BaseList_TR_ResultLine_{}\ item_tr_customstyle > td:nth-child(1) > a:nth-child(1) > img:nth-child(1)".format(str(i)))
            prd_img[prd_id] = img.get_attribute("src")

        prd_id = list(prd_desp)

        for id_ in prd_id:
            prd_desp[id_]["price"] = prd_price[id_]
            prd_desp[id_]["img_link"] = prd_img[id_]


        #print(prd_desp)

        print(page_start, page_total, total)
        #print(prd_price)
        for j in range(0,(page_total-page_start)+1):

            try:
                sleep(3)
                link = driver.find_element_by_css_selector("#BaseList_TR_ResultLine_{}\ item_tr_customstyle > td:nth-child(2) > span:nth-child(1) > a:nth-child(1)".format(str(j)))
                prd_link = link.get_attribute("href")
                #print(link)
                driver.get(prd_link)
                
                sleep(0.5)

            except Exception as e:
                print(e)

            html = driver.find_element_by_tag_name("html")
            html.send_keys(Keys.END)
            sleep(2)

            try:
                item_id = driver.find_element_by_css_selector("#ItemCodeRef").text 
                prd_desp[item_id]["Name"] = driver.find_element_by_css_selector(".item_detail_title_custom > span:nth-child(1)").text
            except:
                prd_desp[item_id]["Name"] = None
                

            try:
                prd_desp[item_id]["Description"] = driver.find_element_by_css_selector(".itemDescriptionCustomInformation").text                
                
            except Exception as e:
                try:
                    prd_desp[item_id]["Description"] = driver.find_element_by_css_selector(".itemDescriptionCustomInformation").text
                except:
                    prd_desp[item_id]["Description"] = None


            try:
                prd_desp[item_id]["Category"] = driver.find_element_by_css_selector(".BreadCrumbcategorytree_activepage").text
            except Exception as e:
                print("Category Error {}".format(e))
                prd_desp[item_id]["Category"] = None

 
            

            
            if item_id in total_ids:
                driver.execute_script("window.history.go(-1)")
                sleep(2)
            else:

                try:
                    

                    sleep(0.5)
                    driver.find_element_by_css_selector("table.itemdetailCustomTable:nth-child(2)")

                    sleep(0.5)
                    table = driver.find_element_by_css_selector("table.itemdetailCustomTable:nth-child(2)")
                    rows_count = len(driver.find_elements_by_xpath("//*[@id=\"msicustomitemtable\"]/tbody/tr"))
                    columns_count = int(len(driver.find_elements_by_xpath("//*[@id=\"msicustomitemtable\"]/tbody/tr/td")) / rows_count)
                    print(rows_count,columns_count)
                    try:
                        labels = []
                        for k in range(3,columns_count+2):
                            #labels.append(driver.find_element_by_css_selector("table.itemdetailCustomTable:nth-child(2) > tbody:nth-child(1) > tr:nth-child({}) > td:nth-child(1)".format(str(k))).text)
                            #total_ids.append(pid)
                            labels.append(driver.find_element_by_css_selector("table.itemdetailCustomTable:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > th:nth-child({})".format(str(k))).text)
                    except:
                        print("Labels Error {}".format(e))
                        
                    for row in range(2,rows_count+1):
                        modifier_dict={}
                        pid = driver.find_element_by_css_selector("table.itemdetailCustomTable:nth-child(2) > tbody:nth-child(1) > tr:nth-child({}) > td:nth-child(1)".format(str(row))).text
                        total_ids.append(pid)
                        for col in range(2, columns_count+1):
                            modifier_dict[labels[col-2]] = driver.find_element_by_css_selector("table.itemdetailCustomTable:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child({})".format(str(col))).text
                        prd_mod[pid] = modifier_dict
                        print("Inside!")
                        
                    
                    #print(prd_mod)
                    driver.execute_script("window.history.go(-1)")
                    sleep(2)
                except Exception as e:
                    print("outside")
                    print("Modifier Error {}".format(e))
                    driver.execute_script("window.history.go(-1)")
                    sleep(2)
                    
        if page_total != total:
            html = driver.find_element_by_tag_name("html")
            html.send_keys(Keys.END)
            sleep(0.3)
            page_counter+=1
            try:
                driver.find_element_by_css_selector("table.ItemsListPaginationTable:nth-child(7) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > a:nth-child({})".format(str(page_counter))).click()
            except:
                driver.execute_script("window.history.go(-1)")
                sleep(2)
                
            
            sleep(1)
            pages = driver.find_element_by_css_selector(".ItemSearchResults_SummaryMessage").text
            
            pages = pages.split("of")
            total = pages[-1].split(".")
            total = int(total[0])
            pt = pages[0].split("-")
            pt_st = pt[0].split(":")
            page_start, page_total = int(pt_st[1]), int(pt[1])
            
            print("Moving onto next page")
            
        else:
            curr_dict = {'Manufacturer_SKU':[],'Product_Name':[],'Product_Description':[],'Product_Category':[],'Product_Subcategory1':[],'Product_Subcategory2':[],'Manufacturer':[],
                            'Brand':[],'Tags':[],'Barcode':[],'Option_1_Label':[],'Option_1_Value':[],'Option_2_Label':[],'Option_2_Value':[],'Option_3_Label':[],'Option_3_Value':[],
                            'Modifier_1_Label':[],'Modifier_1_Value':[],'Modifier_2_Label':[],'Modifier_2_Value':[],'Modifier_3_Label':[],'Modifier_3_Value':[],'Modifier_4_Label':[],
                            'Modifier_4_Value':[],'Modifier_5_Label':[],'Modifier_5_Value':[],'Modifier_6_Label':[],'Modifier_6_Value':[],'Variant_Name':[],'Variant_Description':[],
                            'Suggested_Manufacturer_List_Price':[],'Suggested_Manufacturer_Clearance_Price':[],'Manufacturer_Cost':[],'Distributor_Cost':[],'Distributor_Clearance_Cost':[],
                            'Discount_Purchase_Quantity':[],'Bulk_Discount_Price':[],'Taxable':[],'Publish_Online':[],'B2B_eCommerce':[],'Purchasable_on_Amazon':[],'Pack_Size_Label':[],
                            'Pack_Size_Value':[],'Weight_Unit':[],'Weight_Value':[],'Product_Dimension_Unit':[],'Product_Width':[],'Product_Height':[],'Product_Depth':[],'Fixed_Shipping_Price':[],
                            'Shipping_Condition':[],'Storage_Condition':[],'HS_Code':[],'Ship_From':[],'Country_of_Origin':[],'Search_Keywords':[],'Page_Title':[],'Meta_Keywords':[],
                            'Meta_Description':[],'Image_Filename':[],'Variable_1_Label':[],'Variable_1_Value':[],'Variable_2_Label':[],'Variable_2_Value':[],'Variable_3_Label':[],
                            'Variable_3_Value':[],'Variable_4_Label':[], 'Variable_4_Value':[],'Variable_5_Label':[],'Variable_5_Value':[],'Variable_6_Label':[],'Variable_6_Value':[]
                        }
            try:
                prd_info = list(prd_desp.keys())
                for id_ in prd_info:
                    try:
                        mod = prd_mod[id_]
                        ml = list(mod.keys())
                        vl = list(mod.values())
                    except:
                        ml = ["None"]
                        vl= ["None"]
                    try:
                        curr_dict['Manufacturer_SKU'].append(id_)
                        curr_dict['Product_Name'].append(prd_desp[id_]["Name"])
                        curr_dict['Product_Description'].append(prd_desp[id_]["Description"])
                        curr_dict['Product_Category'].append(prd_desp[id_]["Category"])
                        curr_dict['Image_Filename'].append(prd_desp[id_]["img_link"])
                    except Exception as e:
                        print(e)
                    curr_dict['Product_Subcategory1'].append(None)
                    curr_dict['Product_Subcategory2'].append(None)
                    curr_dict['Manufacturer'].append(name)
                    curr_dict['Brand'].append(None)
                    curr_dict['Tags'].append(None)
                    curr_dict['Barcode'].append(None)
                    curr_dict['Option_1_Label'].append(None)
                    curr_dict['Option_1_Value'].append(None)
                    curr_dict['Option_2_Label'].append(None)
                    curr_dict['Option_2_Value'].append(None)
                    curr_dict['Option_3_Label'].append(None)
                    curr_dict['Option_3_Value'].append(None)
                    
                    
                    try:
                        curr_dict['Modifier_1_Label'].append(ml[0])
                        curr_dict['Modifier_1_Value'].append(vl[0])
                    except Exception as e:
                        print("Modifier_dict Error {}".format(e))
                        curr_dict['Modifier_1_Label'].append(None)
                        curr_dict['Modifier_1_Value'].append(None)

                    try:
                        curr_dict['Modifier_2_Label'].append(ml[1])
                        curr_dict['Modifier_2_Value'].append(vl[1])
                    except Exception as e:
                        print("Modifier_dict Error {}".format(e))
                        curr_dict['Modifier_2_Label'].append(None)
                        curr_dict['Modifier_2_Value'].append(None)

                    try:
                        curr_dict['Modifier_3_Label'].append(ml[2])
                        curr_dict['Modifier_3_Value'].append(vl[2])
                    except Exception as e:
                        print("Modifier_dict Error {}".format(e))
                        curr_dict['Modifier_3_Label'].append(None)
                        curr_dict['Modifier_3_Value'].append(None)
                    try:
                        curr_dict['Modifier_4_Label'].append(ml[3])
                        curr_dict['Modifier_4_Value'].append(vl[3])
                    except Exception as e:
                        print("Modifier_dict Error {}".format(e))
                        curr_dict['Modifier_4_Label'].append(None)
                        curr_dict['Modifier_4_Value'].append(None)

                    try:
                        curr_dict['Modifier_5_Label'].append(ml[4])
                        curr_dict['Modifier_5_Value'].append(vl[4])
                    except Exception as e:
                        print("Modifier_dict Error {}".format(e))
                        curr_dict['Modifier_5_Label'].append(None)
                        curr_dict['Modifier_5_Value'].append(None)

                    try:
                        curr_dict['Modifier_6_Label'].append(ml[5])
                        curr_dict['Modifier_6_Value'].append(vl[5])
                    except Exception as e:
                        print("Modifier_dict Error {}".format(e))
                        curr_dict['Modifier_6_Label'].append(None)
                        curr_dict['Modifier_6_Value'].append(None)


                    
                        

                    curr_dict['Variant_Name'].append(None)
                    curr_dict['Variant_Description'].append(None)
                    curr_dict['Suggested_Manufacturer_List_Price'].append(None)
                    curr_dict['Suggested_Manufacturer_Clearance_Price'].append(None)
                    curr_dict['Manufacturer_Cost'].append(None)
                    curr_dict['Distributor_Cost'].append(prd_desp[id_]["price"])
                    curr_dict['Distributor_Clearance_Cost'].append(None)
                    curr_dict['Discount_Purchase_Quantity'].append(None)
                    curr_dict['Bulk_Discount_Price'].append(None)
                    curr_dict['Taxable'].append(None)
                    curr_dict['Publish_Online'].append(None)
                    curr_dict['B2B_eCommerce'].append(None)
                    curr_dict['Purchasable_on_Amazon'].append(None)
                    curr_dict['Pack_Size_Label'].append(None)
                    curr_dict['Pack_Size_Value'].append(None)
                    curr_dict['Weight_Unit'].append(None)
                    curr_dict['Weight_Value'].append(None)
                    curr_dict['Product_Dimension_Unit'].append(None)
                    curr_dict['Product_Width'].append(None)
                    curr_dict['Product_Height'].append(None)
                    curr_dict['Product_Depth'].append(None)
                    curr_dict['Fixed_Shipping_Price'].append(None)
                    curr_dict['Shipping_Condition'].append(None)
                    curr_dict['Storage_Condition'].append(None)
                    curr_dict['HS_Code'].append(None)
                    curr_dict['Ship_From'].append(None)
                    curr_dict['Country_of_Origin'].append(None)
                    curr_dict['Search_Keywords'].append(None)
                    curr_dict['Page_Title'].append(None)
                    curr_dict['Meta_Keywords'].append(None)
                    curr_dict['Meta_Description'].append(None)
                    curr_dict['Variable_1_Label'].append(None)
                    curr_dict['Variable_1_Value'].append(None)
                    curr_dict['Variable_2_Label'].append(None)
                    curr_dict['Variable_2_Value'].append(None)
                    curr_dict['Variable_3_Label'].append(None)
                    curr_dict['Variable_3_Value'].append(None)
                    curr_dict['Variable_4_Label'].append(None)
                    curr_dict['Variable_4_Value'].append(None)
                    curr_dict['Variable_5_Label'].append(None)
                    curr_dict['Variable_5_Value'].append(None)
                    curr_dict['Variable_6_Label'].append(None)
                    curr_dict['Variable_6_Value'].append(None)

                    product_information = pd.DataFrame(curr_dict)
                    pd.DataFrame(product_information).to_csv('CSVs/SecondRun/{}_FullRun.csv'.format(name))
            except Exception as e:
               print("Dict Error {}".format(e))
            driver.quit()

            return


  

  
if __name__ == "__main__":
    file = open("VenderList.txt", "r")
    line = file.read()
    VenderNames = line.split("\n")
    for vndNme in VenderNames:
        print("Looking for Products of vendor: {}".format(vndNme))
        cnt = count()
        cnt.start()
        product_information(vndNme)
        stats = cnt.finish()
        print("Time Elasped: {} mins : {} secs".format(stats["mins"], stats["secs"]))
    
    
        
    
    
                  
                       

