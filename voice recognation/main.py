import speech_recognition as sr
from gtts import gTTS
import datetime
import os
import pyfiglet



class converter():
    def __init__(
        self,
        folder_name_for_system_can_read_files:str = 'script_to_read',
        language:str='id',
        talk_slower: bool=False,
        user_input_text_output_file_name:str='audio_from_text',
        user_input_file_text_output_file_name:str='audio_from_file_text',
        user_mic_output_file_name:str='text_from_mic'
        ):
        # user mode/user can change this
        self.lang:str = language
        self.talk_type:bool = talk_slower
        self.folder_name_so_system_can_read_files:str = folder_name_for_system_can_read_files
        # dev mode/dev can tweaks this
        self.standart_user_output_name_text_input:str= user_input_text_output_file_name # output file name
        self.standart_user_output_name_file_input:str= user_input_file_text_output_file_name # output file name
        self.standart_user_output_name_mic_input:str= user_mic_output_file_name # output file name

    def text_to_voice(self,your_text:str,output_file_name:str):
        converted = gTTS(your_text,lang=self.lang,slow=self.talk_type)
        if output_file_name:
            converted.save(f'{output_file_name}.mp3')
            print(f'teks berhasil di ubah ke suara\nfile: {output_file_name}.mp3')
        else:
            converted.save(f'{self.standart_user_output_name_text_input}.mp3')
            print(f'teks berhasil di ubah ke suara\nfile: {self.standart_user_output_name_text_input}.mp3')

    def voice_to_text(self,output_file_name:str):
        engine = sr.Recognizer()
        mic = sr.Microphone()
        user_all_word_in_mic:list[str] = []
        while True:
            try:
                with mic as user_voice:
                    print('sedang menyiapkan mic untuk anda...')
                    engine.adjust_for_ambient_noise(mic,0.5)
                    print('silahkan mulai berbicara')
                    print('program akan mencatat apa yang anda bicarakan mulai sekarang...')
                    get_user_voice = engine.listen(user_voice,phrase_time_limit=60)
                    convert_to_plain_text:str = engine.recognize_google(get_user_voice, language="id-ID").lower()
                    print('sedang mengupdate, mohon berhenti berbicara sebentar')
                    if "selesai" in convert_to_plain_text:
                        print('mic di berhentikan')
                        break
                    user_all_word_in_mic.append(convert_to_plain_text)
            except sr.UnknownValueError:
                print('suara anda tidak kedengeran oleh mic, silahkan ulangi kata-kata anda jika anda mau')
            except sr.RequestError:
                print('tolong nyalakan internet anda terlebih dahulu')
            except KeyboardInterrupt:
                print('berhenti paksa')

        if output_file_name:
            with open(f'{output_file_name}.txt','a',encoding='utf-8') as f:
                f.write(f'[{datetime.datetime.now()}]\n' + convert_to_plain_text + '\n\n')
        else:
            with open(f'{self.standart_user_output_name_mic_input}.txt','a',encoding='utf-8') as f:
                f.write(f'[{datetime.datetime.now()}]\n' + convert_to_plain_text + '\n\n')

    def script_text_to_voice(self,output_file_name:str,file_name_script:str):
        full_path_folder_can_access = os.path.join(f'./{self.folder_name_so_system_can_read_files}',f'{file_name_script}.txt')
        
        # cek file di workspace user
        if not os.path.exists(full_path_folder_can_access):
            file_path_to_read_fallback = os.path.join('.',f'{file_name_script}.txt')

            if os.path.exists(file_path_to_read_fallback):
                with open(file_path_to_read_fallback,'r',encoding='utf-8') as f:
                    text_from_file = f.read()
            else:
                print('file gak ada dimanapun')

        # kalo ada text file di folder script
        else:
            with open(full_path_folder_can_access,'r',encoding='utf-8') as f:
                text_from_file = f.read()

        converted = gTTS(text_from_file,lang=self.lang,slow=self.talk_type)
        
        if output_file_name:
            converted.save(f'{output_file_name}.mp3')
            print(f'teks berhasil di ubah ke s PROGRAM KONVERSI TEKS DAN SUARA"\nfile: {output_file_name}.mp3')
        else:
            converted.save(f'{self.standart_user_output_name_file_input}.mp3')
            print(f'teks berhasil di ubah ke suara\nfile: {self.standart_user_output_name_file_input}.mp3')

    def read_all_script_in_folder(self,output_file_name:str,folder_to_read=None):
        full_text:list[str] = []
        if not folder_to_read:
            for files in os.listdir(self.folder_name_so_system_can_read_files):
                every_path_files = os.path.join(self.folder_name_so_system_can_read_files,files)
                if os.path.isfile(every_path_files):
                    with open(every_path_files,'r',encoding='utf-8') as f:
                        print(f'\nsedang mengubah file: {files}')
                        text_to_read = f.read()
                        full_text.append(text_to_read)
                    full_text_str = "".join(full_text) 
                    converted = gTTS(full_text_str,lang=self.lang,slow=self.talk_type)
                    print(f'text file berhasil ditambahkan ke {output_file_name}.mp3')
                if output_file_name:
                    converted.save(f'{output_file_name}.mp3')
                    print(f'teks berhasil di ubah ke suara\nfile: {output_file_name}.mp3')
                else:
                    converted.save(f'{self.standart_user_output_name_file_input}.mp3')
                    print(f'teks berhasil di ubah ke suara\nfile: {self.standart_user_output_name_file_input}.mp3')

    def display_menu(self):
        print(pyfiglet.figlet_format('WELCOME TO CONVERTER PROGRAM'))
        print("="*50)
        print("1. Teks ke Suara (Text to Speech)")
        print("2. Suara ke Teks (Speech to Text)")
        print("3. File Teks ke Suara")
        print("4. Gabungkan Semua File Teks dalam Folder")
        print("5. Pengaturan Program")
        print("6. Bantuan")
        print("7. Keluar")
        print("="*50)

    def func_menu(self):
        """Menjalankan menu utama program"""
        while True:
            self.display_menu()
            choice = input("\nPilih menu (1-7): ").strip()
            
            if choice == "1":
                self.menu_text_to_voice()
            elif choice == "2":
                self.menu_voice_to_text()
            elif choice == "3":
                self.menu_script_text_to_voice()
            elif choice == "4":
                self.menu_read_all_scripts()
            elif choice == "5":
                self.menu_settings()
            elif choice == "6":
                self.menu_help()
            elif choice == "7":
                print("Terima kasih telah menggunakan program ini!")
                break
            else:
                print("Pilihan tidak valid. Silakan pilih 1-7.")

        """gw buat basic nya dulu, baru nanti gw ubah dikit-dikit"""
    def menu_text_to_voice(self):
        user_text = input('masukan text untuk di ubah: ').strip()
        file_output = input('nama file untuk hasil perubahan: ')
        return self.text_to_voice(user_text,file_output)

    def menu_voice_to_text(self):
        file_output = input('mohon masukan nama file untuk hasil perubahan: ').strip()
        print('kami akan menyalakan mic anda saat anda menekan enter')
        input()
        self.voice_to_text(file_output)
    
    def menu_script_text_to_voice(self):
        filename_to_read = input("nama file buat dibaca sistem (sistem otomatis baca di folder anda saat ini atau folder khusus yang sudah anda buat): ").strip()
        file_output = input('nama file buat hasil suara: ').strip()
        return self.script_text_to_voice(file_name_script=filename_to_read,output_file_name=file_output)
        
    def menu_read_all_scripts(self):
        print('jika sudah di setting dari awal biarkan kosong')
        folder_to_read_script = input('nama folder untuk di baca oleh sistem/default folder: ').strip()
        output_file = input('masukan nama file buat hasil perubahannya: ').strip()
        if folder_to_read_script:
            read_folder = folder_to_read_script
        else:
            read_folder = self.folder_name_for_system_can_read_files

        return self.read_all_script_in_folder(output_file_name=output_file,folder_to_read=read_folder)
    
    def menu_settings(self):
        print(f'bahasa saat ini: {self.lang}')
        print(f'folder default saat ini: {self.folder_name_so_system_can_read_file}')
        print('[1] ubah bahasa')
        print('[2] ubah default folder')
        print('[x] exit')
        user = input('>> ').strip()
        if user == '1':
            new_lang = input('bahasa baru: ').strip()
            self.lang = new_lang
            print('bahasa berhasil di ubah')
        elif user == '2':
            new_folder = input('folder default: ').strip()
            self.folder_name_so_system_can_read_file = new_folder
            print('folder berhasil di ubah')

    def menu_help(self):
        pass


conv = converter()
conv.display_menu()