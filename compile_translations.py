import os
import sys
import struct
import array

def msgfmt(filename):
    """
    Generate binary message catalog from textual translation description.

    This function is a simplified version of the Tools/i18n/msgfmt.py
    script from the Python source distribution.
    """
    messages = {}
    
    # Parse the .po file
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    section = None
    msgid = b''
    msgstr = b''
    
    def unescape(s):
        return s.replace('\\n', '\n').replace('\\"', '"').replace('\\t', '\t').replace('\\\\', '\\')

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        if line.startswith('msgid'):
            if section == 'msgstr':
                messages[msgid] = msgstr
                msgid = b''
                msgstr = b''
            section = 'msgid'
            content = line[5:].strip()
            if content.startswith('"') and content.endswith('"'):
                content = content[1:-1]
            msgid += unescape(content).encode('utf-8')
        elif line.startswith('msgstr'):
            section = 'msgstr'
            content = line[6:].strip()
            if content.startswith('"') and content.endswith('"'):
                content = content[1:-1]
            msgstr += unescape(content).encode('utf-8')
        elif line.startswith('"'):
            content = line
            if content.startswith('"') and content.endswith('"'):
                content = content[1:-1]
            
            if section == 'msgid':
                msgid += unescape(content).encode('utf-8')
            elif section == 'msgstr':
                msgstr += unescape(content).encode('utf-8')

    if section == 'msgstr':
        messages[msgid] = msgstr

    # Generate .mo file content
    offsets = []
    ids = b''
    strs = b''
    
    # The header is 7 32-bit integers
    # magic, revision, nstrings, orig_table_offset, trans_table_offset,
    # hash_table_size, hash_table_offset
    
    keys = sorted(messages.keys())
    
    for id in keys:
        offsets.append((len(ids), len(id), len(strs), len(messages[id])))
        ids += id + b'\0'
        strs += messages[id] + b'\0'
        
    output_file = os.path.splitext(filename)[0] + '.mo'
    
    with open(output_file, 'wb') as f:
        # Magic number
        f.write(struct.pack('I', 0x950412de))
        # Revision
        f.write(struct.pack('I', 0))
        # N strings
        f.write(struct.pack('I', len(keys)))
        
        # Offset of original strings table
        off_orig = 28
        f.write(struct.pack('I', off_orig))
        
        # Offset of translation strings table
        off_trans = off_orig + len(keys) * 8
        f.write(struct.pack('I', off_trans))
        
        # Hash table size (0 for now)
        f.write(struct.pack('I', 0))
        # Hash table offset
        f.write(struct.pack('I', 0))
        
        # Original strings table
        start_ids = off_trans + len(keys) * 8
        for o in offsets:
            f.write(struct.pack('II', o[1], start_ids + o[0]))
            
        # Translation strings table
        start_strs = start_ids + len(ids)
        for o in offsets:
            f.write(struct.pack('II', o[3], start_strs + o[2]))
            
        # Strings
        f.write(ids)
        f.write(strs)
        
    print(f"Compiled {filename} -> {output_file}")

def main():
    base_dir = os.path.join(os.getcwd(), 'locale')
    if not os.path.exists(base_dir):
        print("Locale directory not found.")
        return

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.po'):
                full_path = os.path.join(root, file)
                try:
                    msgfmt(full_path)
                except Exception as e:
                    print(f"Error compiling {full_path}: {e}")

if __name__ == '__main__':
    main()
