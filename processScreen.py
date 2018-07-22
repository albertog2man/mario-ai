import numpy as np 
import glob, os
import cv2
import time
from PIL import ImageGrab 
from directKeyMaps import PressKey, W, A, S, D
from templateSource import TemplateSource


class ProcessScreen:
    
    @classmethod
    def run(cls):
        cls().run_loop()

    def run_loop(self):
        self.should_loop = True
        self.import_templates()
        self.stamp_loop_time()
        while(self.should_loop):
            # self.log_fps()
            self.stamp_loop_time()
            self.show_screen()
            self.listen_for_quit()
           
    def show_screen(self):
        cv2.imshow('window', self.process_img())

    def process_img(self):
        image = self.convert_to_grey(self.grab_screen())
        current_template = self.templates[0]
        match_result = cv2.matchTemplate(image,current_template.image,cv2.TM_CCOEFF_NORMED)
        threshold = 0.6
        loc = np.where( match_result >= threshold )
        for pt in zip(*loc[::-1]):
            cv2.rectangle(image, pt, (pt[0] + current_template.width, pt[1] + current_template.height), (0,255,255), 2)
        return image


    def import_templates(self):
        os.chdir("./templateSources")
        self.templates = []
        for file in glob.glob("*.jpg"):
            image = self.convert_to_grey(self.grab_image_from_file(file))
            imageObj = TemplateSource(image)
            self.templates.append(imageObj)

    def grab_image_from_file(self, file):
        return cv2.imread(file)

    def listen_for_quit(self):
         if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                self.should_loop = False

    def grab_screen(self):
        return np.array(ImageGrab.grab(bbox=(0,40,800,640)))    

    def convert_to_grey(self, original):
        return cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

    def stamp_loop_time(self):
        self.loop_time = time.time()

    def log_fps(self):
        print('FPS: {}'.format(self.get_fps()))

    def get_fps(self):
        time_value = time.time()
        if( time_value - self.loop_time ):
            return round(1.0 / (time_value - self.loop_time))
        else:
            return 0 

   