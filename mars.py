from zipfile import ZipFile, BadZipFile
import zlib
import sys, os, time
from tqdm import tqdm
import colorama
import pyfiglet
import random
from datetime import datetime, timedelta
import multiprocessing as mp
from io import BytesIO
import queue

colorama.init(autoreset=True)

COLORS = {
    "HEADER": colorama.Fore.LIGHTMAGENTA_EX,
    "INPUT": colorama.Fore.LIGHTCYAN_EX,
    "INFO": colorama.Fore.LIGHTBLUE_EX,
    "SUCCESS": colorama.Fore.LIGHTGREEN_EX,
    "FAIL": colorama.Fore.LIGHTRED_EX,
    "WARNING": colorama.Fore.LIGHTYELLOW_EX,
    "RESET": colorama.Style.RESET_ALL
}

FONTS = ['doom', 'epic', 'avatar', 'chunky', 'graffiti']

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    font = random.choice(FONTS)
    banner = pyfiglet.figlet_format("MARS-11", font=font, width=os.get_terminal_size().columns)
    print(COLORS["HEADER"] + banner)
    print(COLORS["HEADER"] + "═" * os.get_terminal_size().columns)
    print(f"{COLORS['INFO']} Advanced Archive Password Recovery Tool")
    print(f"{COLORS['INFO']} Version 2.3 | Developed by t.me/MasterX_0\n")

def get_input(prompt):
    return input(f"{COLORS['INPUT']}[?] {prompt}: {COLORS['RESET']}")

def worker_process(zip_data, password_chunk, progress_queue, result_queue):
    try:
        zip_file = ZipFile(BytesIO(zip_data))
        encrypted_files = [f for f in zip_file.filelist if f.flag_bits & 0x1 and f.CRC != 0]
        if not encrypted_files:
            result_queue.put(ValueError("No encrypted files"))
            return
        target_file = encrypted_files[0]
        count = 0

        for pwd in password_chunk:
            count += 1
            try:
                with zip_file.open(target_file, pwd=pwd) as f:
                    data = f.read(1024)
                    crc = zlib.crc32(data)
                    while True:
                        chunk = f.read(4096)
                        if not chunk: break
                        crc = zlib.crc32(chunk, crc)
                    if crc != target_file.CRC:
                        raise RuntimeError("CRC mismatch")

                result_queue.put((pwd, count))
                return
            except:
                pass
            if count % 100 == 0:
                progress_queue.put(count)
                count = 0
        if count > 0:
            progress_queue.put(count)
    except Exception as e:
        result_queue.put(e)

def crack_zip(zip_path, wordlist_path):
    try:
        with open(zip_path, 'rb') as f:
            zip_data = f.read()

        with ZipFile(BytesIO(zip_data)) as zip_file:
            encrypted_files = [f for f in zip_file.filelist if f.flag_bits & 0x1]
            print (f"{COLORS['INFO']}[*] Protected file: {COLORS['WARNING']}{zip_path}")
            print (f"{COLORS['INFO']}[*] Encrypted files: {COLORS['WARNING']}{len(encrypted_files)}")

        with open(wordlist_path, 'r', errors='ignore') as f:
            passwords = [line.strip() for line in f]

        encoded_passwords = []
        invalid_count = 0
        for p in passwords:
            try:
                encoded_passwords.append(p.encode('utf-8', 'replace'))
            except:
                invalid_count += 1

        print (f"{COLORS['INFO']}[*] Total passwords: {len(passwords):,}")
        print (f"{COLORS['INFO']}[*] Valid passwords: {len(encoded_passwords):,}")
        print ()

        num_workers = mp.cpu_count() * 6
        chunk_size = len(encoded_passwords) // num_workers
        chunks = [encoded_passwords[i*chunk_size:(i+1)*chunk_size] for i in range(num_workers)]
        remainder = len(encoded_passwords) % num_workers
        if remainder:
            for i in range(remainder):
                chunks[i].append(encoded_passwords[chunk_size*num_workers + i])

        result_queue = mp.Queue()
        progress_queue = mp.Queue()
        workers = [mp.Process(target=worker_process, args=(zip_data, chunk, progress_queue, result_queue)) 
                  for chunk in chunks]

        for w in workers:
            w.start()

        start_time = time.time()
        found = False
        total = len(encoded_passwords)
        tested_count = 0

        with tqdm(total=total, unit='pass',
                 bar_format=f"{COLORS['INFO']} {{l_bar}}{COLORS['HEADER']}{{bar}}{COLORS['INFO']} {{n_fmt}}/{{total_fmt}}") as pbar:
            while not found and any(w.is_alive() for w in workers):
                try:
                    result = result_queue.get_nowait()
                    if isinstance(result, tuple):
                        password, count = result
                        tested_count += count
                        found = True
                        pbar.update(count)
                    elif isinstance(result, Exception):
                        raise result
                except queue.Empty:
                    pass

                try:
                    while True:
                        cnt = progress_queue.get_nowait()
                        tested_count += cnt
                        pbar.update(cnt)
                except queue.Empty:
                    pass

                time.sleep(0.01)

            if found:
                for w in workers:
                    if w.is_alive():
                        w.terminate()

                try:
                    elapsed = str(timedelta(seconds=int(time.time() - start_time))).split('.')[0]
                    print(f"\n{COLORS['SUCCESS']}╒══════════════════════════════════════╕")
                    print(f"{COLORS['SUCCESS']}│     PASSWORD FOUND SUCCESSFULLY!     │")
                    print(f"{COLORS['SUCCESS']}╘══════════════════════════════════════╛")
                    print(f"\n{COLORS['WARNING']}╭──────────────────────────────────────╮")
                    print(f"{COLORS['WARNING']}│  Password: {COLORS['SUCCESS']}{password.decode().ljust(24)} {COLORS['WARNING']} ")
                    print(f"{COLORS['WARNING']}│  Tested: {COLORS['INFO']}{tested_count}/{total} passwords".ljust(35) + f"{COLORS['WARNING']} ")
                    print(f"{COLORS['WARNING']}│  Time elapsed: {COLORS['INFO']}{elapsed}".ljust(35) + f"{COLORS['WARNING']} ")
                    print(f"{COLORS['WARNING']}╰──────────────────────────────────────╯\n")
                    return True
                except Exception as e:
                    print(f"{COLORS['FAIL']}[!] Verification failed: {str(e)}")
                    return False
            else:
                print(f"\n{COLORS['FAIL']}╒══════════════════════════════════════╕")
                print(f"{COLORS['FAIL']}│      PASSWORD NOT FOUND!             │")
                print(f"{COLORS['FAIL']}╘══════════════════════════════════════╛")
                return False

    except Exception as e:
        print(f"\n{COLORS['FAIL']}[!] Error: {str(e)}")
        return False

def main():
    print_banner()
    zip_path = get_input("Enter ZIP file path")
    wordlist_path = get_input("Enter password list path")

    if not os.path.exists(zip_path):
        print (f"{COLORS['FAIL']}[!] ZIP file not found!")
        return
    if not os.path.exists(wordlist_path):
        print (f"{COLORS['FAIL']}[!] Wordlist file not found!")
        return

    crack_zip(zip_path, wordlist_path)

    input(f"\n{COLORS['INFO']}Press enter to exit...")
    print ()

if __name__ == "__main__":
    mp.freeze_support()
    main()
