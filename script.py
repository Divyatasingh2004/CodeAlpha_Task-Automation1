import os
import shutil

def process_images(source_folder, destination_folder, operation='move'):
    # Check karo ki source folder exist karta hai ya nahi
    if not os.path.exists(source_folder):
        print(f"\033[1;31mError: Source folder '{source_folder}' nahi mila!\033[0m")
        return

    # Agar destination folder nahi hai, toh use naya bana do
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print(f"\033[1;32mDestination folder naya ban gaya: {destination_folder}\033[0m")
    
    try:
        files = os.listdir(source_folder)
    except Exception as e:
        print(f"\033[1;31mError: Source folder ko read karne mein samasya aayi: {e}\033[0m")
        return

    processed_count = 0
    skipped_count = 0
    error_count = 0
    total_size_bytes = 0
    
    # Supported image extensions (Aap apni zaroorat ke hisab se aur bhi add kar sakte hain)
    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.gif')
    
    print("\n\033[1;36mFiles process ho rahi hain...\033[0m")
    print("-" * 50)
    
    for file in files:
        source_path = os.path.join(source_folder, file)
        
        # Agar yeh koi directory/folder hai, toh isse skip kar do
        if os.path.isdir(source_path):
            skipped_count += 1
            continue
            
        # File extension check karo (case-insensitive)
        if file.lower().endswith(valid_extensions):
            destination_path = os.path.join(destination_folder, file)
            
            # Agar destination mein same naam ki file pehle se hai toh naam rename kar do
            if os.path.exists(destination_path):
                base, ext = os.path.splitext(file)
                counter = 1
                while True:
                    new_filename = f"{base}_{counter}{ext}"
                    destination_path = os.path.join(destination_folder, new_filename)
                    if not os.path.exists(destination_path):
                        break
                    counter += 1
                print(f"\033[1;33m[DUPLICATE] Rename kiya: {file} -> {os.path.basename(destination_path)}\033[0m")
            else:
                action_label = "Copied" if operation == 'copy' else "Moved"
                print(f"\033[1;32m[{action_label}] {file}\033[0m")
            
            # File ko copy ya move karne ki koshish karein (Exception handling ke sath)
            try:
                file_size = os.path.getsize(source_path)
                
                if operation == 'copy':
                    shutil.copy2(source_path, destination_path)
                else:
                    shutil.move(source_path, destination_path)
                
                processed_count += 1
                total_size_bytes += file_size
            except Exception as e:
                error_count += 1
                print(f"\033[1;31m[ERROR] '{file}' ko process nahi kar paaye: {e}\033[0m")
        else:
            skipped_count += 1
            
    # Total size ko MB mein convert karna
    total_size_mb = total_size_bytes / (1024 * 1024)
    
    # Summary Report print karo
    print("-" * 50)
    print("        ENHANCED TASK AUTOMATION SUMMARY REPORT")
    print("-" * 50)
    action_name = "Copied" if operation == 'copy' else "Moved"
    print(f" Total image files {action_name.lower()}    : {processed_count}")
    print(f" Other/Non-image files skipped : {skipped_count}")
    print(f" Errors encountered            : {error_count}")
    print(f" Total data transferred        : {total_size_mb:.2f} MB")
    print("-" * 50)
    print("\033[1;32mKaam safalpurvak pura ho gaya hai!\033[0m")

if __name__ == "__main__":
    print("=== Advanced Python Task Automation Script ===")
    src_dir = input("Source folder ka path enter karo: ").strip()
    dest_dir = input("Destination folder ka path enter karo: ").strip()
    
    # User se pucho ki move karna hai ya copy
    op_choice = input("Kya aap files ko Move karna chahte hain ya Copy? (m/c - Default is move): ").lower().strip()
    operation = 'copy' if op_choice == 'c' else 'move'
    
    process_images(src_dir, dest_dir, operation)