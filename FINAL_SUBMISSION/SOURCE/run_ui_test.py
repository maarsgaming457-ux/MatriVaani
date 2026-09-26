import uiautomator2 as u2
import time
import sys
import io

# force utf8 stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def run_test(text):
    d = u2.connect()
    
    # check for translator screen
    if d(description="Translator").exists(timeout=2):
        d(description="Translator").click()
    
    time.sleep(2)
    
    input_box = d(className="android.widget.EditText")
    input_box.click()
    time.sleep(1)
    
    # dismiss any google keyboard dialogs
    if d(text="OK").exists(timeout=1):
        d(text="OK").click()
    
    input_box.set_text(text)
    time.sleep(1)
    
    # Hide keyboard so translate button is visible/clickable
    d.press("back")
    time.sleep(1)
    
    translate_btn = d(description="Translate")
    translate_btn.click()
    
    print(f"Sent text: {text}")
    
    start_time = time.time()
    while time.time() - start_time < 20:
        time.sleep(1)
        xml = d.dump_hierarchy()
        if 'Error:' in xml or ('...' not in xml):
            break
            
    time.sleep(2)
    
    xml = d.dump_hierarchy()
    print("FINISHED")
    print(xml)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_test(sys.argv[1])
    else:
        run_test("नमस्ते बच्चों, आज हम गिनती सीखेंगे।")
