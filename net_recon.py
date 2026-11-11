 
# ⚔️ التدريب الهندسي (التحدي النهائي للمستوى الثاني)
import socket 

# هنا سنكتب LIST فارغ  بها الاشياء التي نريد ان نظيفة
start_end_port = [] # بداية ونهاية البورت 

open_port = [] # البروتات المفتوحه
close_port = [] # البروتات المغلقة 

# الset للتنظيف بدون تكرار
set_port = set()



while True :
    equ = "=="*20
    print(equ)
    print("1-Add ip\n2-Show\n3-Exit")
    print(equ)

    choice = input("Enter chocie number : ").strip()

    if choice == "1" :
        target_ip = input("Enter IP target : ").strip()


        # == الدفاعات ==

        # 1) اذا كان فارغ
        if not target_ip :
            print("It must be not empty.")
            continue 

        
        
        part = target_ip.split(".") 

        if not len(part) == 4:
            print("[!] Error: Invalid IP format. It must consist of exactly 4 parts (e.g., 192.168.1.1).")
            continue

        clear_port = [] 
        is_valid = True 
        for p in part : 

            if not p.isdigit()  : # اذا لم يكن عدد صحيح 
                is_valid = False 
                break

            int_part = int(p)

            if int_part < 0 or int_part > 255 :
                is_valid = False 
                break

            # اذا اجتاج هذه الامور  اعطيني ايبي نضيف وضيفة للقائمة 
            clear_port.append(str(int_part))
            # هنا قام بأضافته 

        if not is_valid :  # اذا لم يتحقق الشرطين السابقين 
            print("The number must be between 0 and 255.") 
            continue

        

        # هنا يجب ان نستخرج ايبي نظيف خالي من اي صفار
        clean_ip = ".".join(clear_port)

        print(f"Finally IP : {clean_ip}")
        # هنا ننتهي من الايبي 
        #############################################################################################

        # 2) port 
        
        start_port = input("Enter the starting port you wish to scan : ").strip() # بداية البورت من اين يفحص
        if not start_port : 
            print("It must be not empty.")
            continue

        if not start_port.isdigit() :
            print("It must be numbers only.")
            continue

        int_start = int(start_port)

        if int_start < 0 or int_start > 65535 : 
            print("The numbers should be between (0-65535).")
            continue


        end_port = input("Enter the end of the port range you wish to scan : ").strip() # نهاية البورت اين ينتهي الفحص


        if not end_port : 
            print("It must be not empty.")
            continue

        if not end_port.isdigit() :
            print("It must be numbers only.")
            continue

        int_end = int(end_port)

        if int_end < 0 or int_end > 65535 : 
            print("The numbers should be between (0-65535).")
            continue
        # هنا انتهى من الدفاعات البورت port



        for se in range(int_start , int_end + 1)  :

            set_port.add(se) # هنا سيأمن عدم تكرار الارقام 

        for soc in set_port :
            print(f"\n[*] Trying to connect to {clean_ip} on port {soc}...")

            result_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM) # هنا يتصل بالسيرفر 

            timeout = 0.5 

            result_time = result_socket.settimeout(timeout)

            print(f"Waiting '{timeout}'Second for the connection to the server")

            check_status = result_socket.connect_ex((clean_ip , soc))

            if check_status == 0 : # اذا كان مفتوح 
                open_port.append(soc)

            else : 
                close_port.append(soc)

            result_socket.close()
    elif choice == "2" :

        # ==========================================
        # مرحلة طباعة التقرير النهائي (Reporting)
        # ==========================================
        equ = "=="*20
        print(equ)
        print(f"=== Scan Report for IP: {clean_ip} ===")
        print(equ)

        print(equ)
        print("\n[+] OPEN PORTS:")

        if len(open_port) > 0 :
            count = 1 
            for open_s in open_port : 
                print(f"{count}-Port : {open_s}")
                count += 1 

        print(equ)
        print("\n[+] CLOSED PORTS:")
        if len(close_port) > 0 :
            count = 1 
            for close_s in close_port :
                print(f"{count}-Port : {close_s}")
                count += 1
