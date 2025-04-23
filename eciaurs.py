import struct
import sys
import os
import zlib
import urllib.request
import ast
import threading

print('Eric's Chicken invaders Assets Unpacking and Repacking script\n©2025 Ericbruh / Marisa Kirisame')
mode = input('chose mode:(1: unpack, 2: repack): ')
table = 'https://file.garden/Z2lW4yuyMSaHkbSp/map.txt'
s = urllib.request.build_opener()
s.addheaders = [('User-Agent', "reimu/1.0")]
urllib.request.install_opener(s)

with urllib.request.urlopen(table) as response:
    data = response.read().decode()
    c = ast.literal_eval(data)

def read_u32(f):
    return struct.unpack("<I", f.read(4))[0]

def extract(filename, output_dir="."):
    print(output_dir)
    with open(filename, "rb") as f:
        test = f.read(4)
        if test != b"UVE ":
            raise ValueError("fuxk you this is not valid uve wad4 dule or smth")
        f.read(4)
        f.read(4)
            
        num_files = read_u32(f)
        e = []
        for _ in range(num_files):
            name_crc = read_u32(f)
            name = f"{name_crc:08x}"
            name.replace('.', '')
            
            #print(name)
            if c.get(str(name).lower()) != None and c.get(str(name).lower()) != ' ':
            	print('replacing name...')
            	name = c.get(str(name).lower())
            	print(name)
            offset = read_u32(f)
            zsize = read_u32(f)
            size = read_u32(f)
            offsettable(f"{name_crc:08x}".lower().replace(".", ''), offset, size, zsize, '/sdcard/')
            e.append((name, offset, zsize, size))

        # Extract each file
        for name, offset, zsize, size in e:
            f.seek(offset)
            data = f.read(zsize)

            if size != zsize:
                try:
                    data = zlib.decompress(data)
                except zlib.error as e:
                    pass
                    continue
            output_file = str(name).replace("[", "").replace("'", '').replace("]", "")
            output_path = os.path.dirname(output_file)
            if output_path != '/sdcard':
            	os.makedirs(os.path.join(output_dir, output_path), exist_ok=True)
            	try:
            		with open(os.path.join(output_dir, output_file), "wb") as out_file:
            			out_file.write(data)
            			print(f"Extracted: {name}")
            	except:
            		pass
            else:
            	print('skipping...')

def repack(f):
	o = 0
	r = 0
	with open(f, 'rb+') as j:
		test = j.read(4)
		if test != b"UVE ":
			print('my brother i told you to give me a WAD4 file')
		else:
			j.read(8)
			inputted_file = input('gimme your input file: ')
			#inputted_file = "/sdcard/a.mp3"
			esize = os.path.getsize(inputted_file)
			
			replacing = input("tell me the file to be replaced: (ex: music/quiet.ogg): ")
			#replacing = "music/intense.ogg"
			data1 = None
			with open(inputted_file, "rb") as t:
				_ = t.read()
				data1 = _
			file_num = read_u32(j)
			e = []
			for marisa in range(file_num):
				pos = j.tell()
				name_crc = read_u32(j)
				name = f"{name_crc:08x}"
				offset = read_u32(j)
				zsize_pos = j.tell()
				zsize = read_u32(j)
				size_pos = j.tell()
				size = read_u32(j)
				e.append((name, offset, zsize, size, zsize_pos, size_pos))
			for name, offset, size, zsize, zsize_pos, size_pos in e:
				result = str(c.get(str(name).lower())).replace("[", "").replace("'", '').replace("]", '')
				#print(result)
				if result is not None and result == replacing:
					print(j.tell())
					j.seek(offset)
					j.write(data1)
					if esize < zsize:
						j.write(b'\x00' * (zsize - esize))
					j.seek(zsize_pos)
					j.write(struct.pack('<I', esize))
					j.seek(size_pos)
					j.write(struct.pack('<I', esize))
					print('Rewritten and repacked!')
					r = r + 1
					
				elif result is not None and replacing not in result:
					pass
				else:
					pass
if mode == '1':
	path = input('gimme ur 222x stuff: ')
	os.makedirs(os.path.join(os.path.dirname(path), 'extracted/'), exist_ok=True)
	out = os.path.join(os.path.dirname(path), 'extracted/')
	extract(path, out)
	
elif mode == '2':
	path = input('gimme ur 222x stuff: ')
	repack(path)
else:
	print('Invalid. Chose again')
	
