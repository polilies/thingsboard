from classes import *



def main() -> None:
    devices, ips, indxes = read_conf_sep()
    
    
    let = True
    while True:
        if (get_minute() in minutes) and let:
            looper(devs=devices, ips=ips, index_list=indxes)
            let = False
        elif get_minute() not in minutes:
            let = True
        
        time.sleep(30)


if __name__ == '__main__':
    main()