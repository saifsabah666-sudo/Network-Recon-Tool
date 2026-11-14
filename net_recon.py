import socket
import json
# الدالة الاولى 
def get_service_name(port_num) :
    unknown = {9999 : "Proxy" , 8080 : "Backdoor" , 4444  : "Metasploit"} 
    try :

        result_socket =  socket.getservbyport(port_num , "tcp")

        return result_socket 

    except :

        if port_num in unknown :
            # إذا كان الرقم موجوداً في القاموس، أرجع قيمته
            return unknown[port_num]

        else : 
            # إذا لم يكن في نظام التشغيل ولا في قاموسنا، نرجع هذه الكلمة
            return "Unknown Service"


clear_ip = ""        
while True : 
    try :
            
        equ = "=="*20
        print(equ)
        print("1-Scan target\n2-Export to Json\n3-Export to TXT\n4-Exit")
        print(equ)
        choice = input("Enter choice number : ").strip()

        if choice == "1" :
            
            set_port = set() # الايبيات النظيفة 

            open_port = [] # البورتات المفتوحه
            close_port = [] # البورتات الممغلقة 


            ip_target = input("Enter target ip : ").strip()

            if not ip_target : 
                print("It must be not empty.")
                continue


            part_ip = ip_target.split(".")

            if not len(part_ip) == 4 :
                print("It must consist of four parts.")
                continue 

            # بما انه متكون من 4 اجزاء 
            clean_ip = []
            is_valid = True
            for p in part_ip : 
                if not p.isdigit() :
                    is_valid = False
                    break

                int_ip = int(p)

                if int_ip < 0 or int_ip > 255 : 
                    is_valid = False 
                    break

                clean_ip.append(str(int_ip)) # لازم يكون string حتى ينظف من الاصفار 

            if not is_valid :
                print("There must be between 0-255")
                continue
            # ذا تخطى كل الشروط
            clear_ip = ".".join(clean_ip)
            print(type(clear_ip))
            print(f"Reuslt IP : {clear_ip}")
            # دفاعات اايبي 
            ################################################################################

            # 2) الان البورتات 
            start_port =input("Enter start port :").strip()

            if not start_port : 
                print("The port must not be empty.")
                continue

            if not start_port.isdigit() : 
                print("It must be number only.")
                continue

            int_start_port = int(start_port)

            if int_start_port < 0 or int_start_port > 65535 :
                print("The port must be between 0-65535")
                continue
            # جزء الاول من البورت خلص 

            # الجزء النهائي
            end_port = input("Enter end port : ").strip()

            if not end_port : 
                print("The port must not be empty.")
                continue

            if not end_port.isdigit() : 
                print("It must be number only.")
                continue 

            int_end_port = int(end_port)

            if int_end_port < 0 or int_end_port > 65535 : 
                print("The port must be between 0-65535")
                continue

            for port_start_end in range(int_start_port , int_end_port + 1) :

                set_port.add(port_start_end) # هنا يضمن عدم تكرار الايبيات 
                # عندما نفتح االحلقة يجب ان نفتح socket
                result_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM) # 

                time_out = 0.5 # هنا توقيت زمني حتى لا يتجمد 
                result_socket.settimeout(time_out) # عنا استدعينا كم الوقت بين كل عملية وعملية 
                print(f"Connecting to the IP {clear_ip} on port {port_start_end}")

                check = result_socket.connect_ex((clear_ip , port_start_end)) #هنا يقوم بالاتصال المخفي الهادئ

                # يرجع اذا كان مفتح يرجع 1
                if check == 0 :
                    open_port.append(port_start_end)

                else :
                    close_port.append(port_start_end)


                # والاخير نغلقت الاتصال 
                result_socket.close()
            print("The ports have been checked.")

        elif choice == "2" :
            if not clear_ip :
                print("Empty; no target specified.")
                continue


            # المستخدم هو من يدخل الاسم الملف 
            file_name = input("Enter file name (without .json) : ").strip()

            

            if not file_name : # يجب ان لا يكون فارغ
                print("File name is empty.")
                continue


            if file_name.isdigit() : # اذا كان الاسم من ارقام صافية فقط
                print("The file name must not consist of numbers.")
                continue

            file = f"{file_name}.json"


            radar_data = {
                "clear_ip" : clear_ip ,
                "open_port" : open_port , 
                "close_port" : len(close_port)
                        } 

            # 2. تجهيز حاوية فارغة للبيانات (القديمة + الجديدة)
            all_scan = []

            try :
                with open(file , "r") as read_json :
                    all_scan = json.load(read_json) # جلب البيانات القديمة

            except (FileNotFoundError , json.JSONDecodeError) : # إذا الملف غير موجود، لا تفعل شيئاً، الحاوية ستبقى فارغة
                pass

            # 4. دمج الهدف الجديد مع الأهداف القديمة
            all_scan.append(radar_data)
                
            # 5. الحفظ النهائي الآمن
            # غرفة العمليات 
            try : 
                with open(file , "w") as file_json : # لفتح الملف بصلاحية الكتابة.
                    json.dump(all_scan , file_json ,indent = 4)
                    print(f"Success! Target saved/appended to {file}")

            except TypeError :
                print("Error: The data structure contains unsupported formats (like sets).")

            except PermissionError : 
                print("Error: Permission denied to write in this location.")

            except OSError as e : 
                print(f"OS Error: Could not save the file due to system restrictions. ({e})")


            except Exception as e :
                print("Error: Could not save the file.")



        elif choice == "3" : 
            if not clear_ip : 
                print("Empty: no target specified.")
                continue
            file_txt = input("Enter name file (without .txt) : ").strip() 

            if not file_txt : 
                print("It must no be empty.")
                continue

            if file_txt.isdigit() :
                print("The file name must not consist of numbers.")
                continue

            final_file_txt = f"{file_txt}.txt" 

            print(f"A file has been created with the name '{final_file_txt}'.")

            domain = input("Enter the target domain name : ").strip()

            if not domain : 
                print("It must be not empty.")
                continue 

            if domain.isdigit() : 
                print("The domain name must be the website's domain name.")
                continue

            print("The website domain was successful.")
            print(f"Domain : {domain}")


            # نفتح السيطرة 
            try : 
                with open(final_file_txt , "a") as target : 
                    # 1. طباعة رأس التقرير (Header)
                    target.write(equ + "\n")
                    target.write("        INTELLIGENCE RADAR REPORT        \n")
                    target.write(equ + "\n")


                    # 2. طباعة الهدف وعدد البورتات المغلقة
                    target.write("===== TARGET INFO =====\n")
                    target.write(f"===== {domain} =====\n")
                    target.write(f"Target IP : {clear_ip}\n")
                    target.write(f"Close Port count : {len(close_port)}\n")
                    target.write(f"{equ}\n")

                    # 3. طباعة البورتات المفتوحة (هنا نستدعي الدالة النائمة!)
                    target.write(f"===== OPEN PORTS & SERVICES =====\n")
                    # نفتح حلقة للمرور على قائمة البورتات المفتوحة
                    target.write(f"{equ}\n")
                    count = 1
                    for p in open_port : 

                        service = get_service_name(p) # نستدعي الدالة ونعطيها رقم البورت، ونخزن النتيجة في المتغير service

                        # نكتب النتيجة في الملف النصي بشكل مرتب
                        target.write(f"{count}-Port : {p:<5} | Service : {service:<5}\n")
                        count +=1
                    target.write(f"{equ}\n\n")# إضافة مسافتين فارغتين في النهاية ليفصل بين التقرير الأول والثاني
            except TypeError : 
                print("Error: The data structure contains unsupported formats (like sets).")

            except PermissionError : 
                print("Error: Permission denied to write in this location.")

            except OSError as e: 
                print(f"OS Error: Could not save the file due to system restrictions. ({e})")

            except Exception as e:
                print(f"Error: Could not save the file {e}.")





        elif choice == "4" :
            print("Exit Radar.")
            break

        else :
            print("You must choose one of the numbers.")
            continue
        

    except KeyboardInterrupt  :
        print()
        print(equ,"\n")
        print("[!] Emergency Exit Triggered (Ctrl+C).")
        print("[!] Exiting Radar safely... Goodbye!")
        print(equ,"\n")
        break

    except Exception as FatalError:
        print(f"\n[!] A fatal system error occurred: {FatalError}")
        print("Please restart the radar.")
        break
