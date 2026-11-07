import os
import random
import tkinter as tk
from PIL import Image, ImageTk

class MikasaPerfectPet:
    def __init__(self, root):
        self.root = root
        
        # 1. إعدادات النافذة بدون إطار وتثبيتها في المقدمة كلياً
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        
        # أبعاد العرض والارتفاع الثابتة للشخصية
        self.width = 200
        self.height = 200
        self.target_size = (self.width, self.height)
        
        # لون الكروما الآمن والأصيل (الماجنتا الساطع)
        self.chroma_color = "#ff00ff"
        self.root.config(bg=self.chroma_color)
        
        # 2. تفعيل الشفافية المستقرة 100% باستخدام ميزة Tkinter الرسمية
        self.root.wm_attributes('-transparentcolor', self.chroma_color)
        
        # 3. حساب حدود وأبعاد الشاشة وموقع البدء الابتدائي المستقر فوق شريط المهام تماماً
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.x = 600
        
        # تم تعديل الفجوة السفلية لتهبط ميكاسا وتلامس شريط المهام تماماً بدلاً من الطيران
        self.floor_gap = 10  
        self.y = self.screen_height - self.height - self.floor_gap
        
        self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        
        # 4. تحميل الحركات وتقطيعها مع تطبيق قناع الحماية الصارم للحواف واللون الفوشيا
        self.animations = {
            'walk': self.load_sprite_clean_edge('image.png', cols=3, rows=3, max_frames=8),
            'sit': self.load_sprite_clean_edge('image (1).png', cols=2, rows=2, max_frames=3),
            'action': self.load_sprite_clean_edge('image (2).png', cols=2, rows=3, max_frames=4),
            'special': self.load_sprite_clean_edge('image (3).png', cols=3, rows=3, max_frames=8)
        }
        
        self.current_action = 'walk'
        self.frame_index = 0
        self.direction = 1  # 1 لليمين، -1 لليسار
        self.is_grabbed = False
        
        # 5. استخدام Label بدلاً من Canvas لمنع الوميض والاهتزاز كلياً
        self.image_label = tk.Label(self.root, bg=self.chroma_color, bd=0, highlightthickness=0)
        self.image_label.pack(fill="both", expand=True)
        
        # بناء قائمة الخيارات عند الضغط كليك يمين
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="❌ إغلاق ميكاسا", command=self.root.destroy)
        
        # ربط أحداث الماوس بالتسمية مباشرة
        self.image_label.bind("<Button-1>", self.start_grab)
        self.image_label.bind("<B1-Motion>", self.drag)
        self.image_label.bind("<ButtonRelease-1>", self.end_grab)
        self.image_label.bind("<Button-3>", self.show_context_menu)
        self.image_label.bind("<Enter>", self.on_mouse_enter)
        self.image_label.bind("<Leave>", self.on_mouse_leave)
        
        # انطلاق المحرك الفيزيائي والأنيميشن مباشرة وبأمان تام
        self.update_behavior()
        self.update_animation()

    def load_sprite_clean_edge(self, file_name, cols, rows, max_frames):
        """تقطيع شبكة الصور واستبدال الأبيض تماماً بخلفية ماجنتا صافية يقصها الويندوز"""
        frames_normal = []
        frames_flipped = []
        
        if not os.path.exists(file_name):
            blank = ImageTk.PhotoImage(Image.new("RGBA", self.target_size, (255, 0, 255, 255)))
            return {'normal': [blank], 'flipped': [blank]}
            
        with Image.open(file_name) as sheet:
            sheet = sheet.convert("RGBA")
            sheet_w, sheet_h = sheet.size
            
            frame_w = sheet_w // cols
            frame_h = sheet_h // rows
            
            count = 0
            for r in range(rows):
                for c in range(cols):
                    if count >= max_frames:
                        break
                        
                    left = c * frame_w
                    top = r * frame_h
                    right = left + frame_w
                    bottom = top + frame_h
                    
                    frame = sheet.crop((left, top, right, bottom))
                    
                    # صبغ بكسلات الخلفية البيضاء أو الشفافة بالماجنتا الصافي المعتم مئة بالمئة
                    data = frame.getdata()
                    new_data = []
                    
                    for item in data:
                        r_pix, g_pix, b_pix, a_pix = item
                        if (r_pix > 230 and g_pix > 230 and b_pix > 230) or a_pix < 50:
                            new_data.append((255, 0, 255, 255))
                        else:
                            new_data.append((r_pix, g_pix, b_pix, 255))
                            
                    frame.putdata(new_data)
                    
                    # عمل Resize بعد التلوين المباشر
                    frame_resized = frame.resize(self.target_size, Image.Resampling.LANCZOS)
                    
                    # خوارزمية التطهير الحاسم: سحق درجات الحواف المتداخلة وتحويلها لكروما نقية تماماً
                    resized_data = frame_resized.getdata()
                    pure_data = []
                    for item in resized_data:
                        r_pix, g_pix, b_pix, a_pix = item
                        # تحويل أي بكسل هجين يحتوي على درجة وردية/بنفسجية طرفية إلى كروما حادة ومثالية ليخفيها النظام
                        if (r_pix > 180 and b_pix > 180 and g_pix < 130) or (r_pix > 235 and g_pix > 235 and b_pix > 235):
                            pure_data.append((255, 0, 255, 255))
                        else:
                            pure_data.append(item)
                    frame_resized.putdata(pure_data)
                    
                    frames_normal.append(ImageTk.PhotoImage(frame_resized))
                    
                    # إنتاج النسخة المعكوسة
                    frame_flipped_img = frame_resized.transpose(Image.FLIP_LEFT_RIGHT)
                    frames_flipped.append(ImageTk.PhotoImage(frame_flipped_img))
                    
                    count += 1
                    
        return {'normal': frames_normal, 'flipped': frames_flipped}

    def on_mouse_enter(self, event):
        if not self.is_grabbed and self.current_action != 'action':
            self.current_action = 'special'
            self.frame_index = 0

    def on_mouse_leave(self, event):
        if not self.is_grabbed and self.current_action == 'special':
            self.current_action = 'walk'
            self.frame_index = 0

    def start_grab(self, event):
        self.is_grabbed = True
        self.current_action = 'action'
        self.frame_index = 0
        self.offset_x = event.x
        self.offset_y = event.y

    def drag(self, event):
        if self.is_grabbed:
            self.x = self.root.winfo_x() + event.x - self.offset_x
            self.y = self.root.winfo_y() + event.y - self.offset_y
            self.root.geometry(f"+{self.x}+{self.y}")

    def end_grab(self, event):
        self.is_grabbed = False

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def update_behavior(self):
        target_floor_y = self.screen_height - self.height - self.floor_gap
        
        if not self.is_grabbed and self.y < target_floor_y:
            self.current_action = 'action'
            self.y += 12
            if self.y >= target_floor_y:
                self.y = target_floor_y
                self.current_action = 'walk'
                self.frame_index = 0
            self.root.geometry(f"+{self.x}+{self.y}")
            
        elif not self.is_grabbed and self.current_action == 'walk':
            self.x += self.direction * 4
            
            if self.x <= 0:
                self.x = 0
                self.direction = 1
            elif self.x >= self.screen_width - self.width:
                self.x = self.screen_width - self.width
                self.direction = -1
                
            self.root.geometry(f"+{self.x}+{self.y}")
            
            if random.randint(1, 500) == 7:
                self.current_action = 'sit'
                self.frame_index = 0
                self.root.after(2500, self.return_to_walk)

        self.root.after(80, self.update_behavior)

    def return_to_walk(self):
        if not self.is_grabbed and self.current_action == 'sit':
            self.current_action = 'walk'
            self.direction = random.choice([1, -1])
            self.frame_index = 0

    def update_animation(self):
        action_data = self.animations[self.current_action]
        
        is_flipped_walk = (self.current_action in ['walk', 'special'] and self.direction == -1)
        current_frames = action_data['flipped'] if is_flipped_walk else action_data['normal']
            
        if self.frame_index >= len(current_frames):
            self.frame_index = 0
            
        my_frame = current_frames[self.frame_index]
        
        self.image_label.configure(image=my_frame)
        self.image_label.image = my_frame
        
        self.frame_index = (self.frame_index + 1) % len(current_frames)
        
        speeds = {'action': 120, 'special': 140}
        anim_speed = speeds.get(self.current_action, 180)
            
        self.root.after(anim_speed, self.update_animation)

if __name__ == "__main__":
    root = tk.Tk()
    pet = MikasaPerfectPet(root)
    root.mainloop()
