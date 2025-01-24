import pygame
import socket
import imp
import subprocess
import re


def draw_knob_slider(screen, eyesy, offx, offy, index) :
    if eyesy.knob_override[index]:
        color = eyesy.RED
    else :
        color = eyesy.LGRAY
    pygame.draw.line(screen, color, [offx, offy], [offx + 16, offy], 1)
    pygame.draw.line(screen, color, [offx, offy], [offx, offy + 40], 1)
    pygame.draw.line(screen, color, [offx + 16, offy], [offx + 16, offy + 40], 1)
    pygame.draw.line(screen, color, [offx, offy + 40], [offx + 16, offy + 40], 1)
    pygame.draw.rect(screen, color, (offx, offy + 40 - int(40*eyesy.knob[index]), 16, int(40*eyesy.knob[index])))

def draw_knob_slider_480(screen, eyesy, offx, offy, index) :
    if eyesy.knob_override[index]:
        color = eyesy.RED
    else :
        color = eyesy.LGRAY
    pygame.draw.line(screen, color, [offx, offy], [offx + 10, offy], 1)
    pygame.draw.line(screen, color, [offx, offy], [offx, offy + 24], 1)
    pygame.draw.line(screen, color, [offx + 10, offy], [offx + 10, offy + 24], 1)
    pygame.draw.line(screen, color, [offx, offy + 24], [offx + 10, offy + 24], 1)
    pygame.draw.rect(screen, color, (offx, offy + 24 - int(24*eyesy.knob[index]), 10, int(24*eyesy.knob[index])))


def draw_vu(screen, eyesy, offx, offy):
    color = eyesy.LGRAY
    for i in range(0,15) :
        x = offx + 14 * i
        pygame.draw.line(screen, color, [x, offy], [x + 10, offy], 1)
        pygame.draw.line(screen, color, [x, offy], [x, offy + 30], 1)
        pygame.draw.line(screen, color, [x + 10, offy], [x + 10, offy + 30], 1)
        pygame.draw.line(screen, color, [x, offy + 30], [x + 10, offy + 30], 1)
    color = eyesy.GREEN
    for i in range(0, eyesy.audio_peak / 2048):
        if i > 8 : color = (255,255,0)
        if i == 14 : color = eyesy.RED
        x = offx + 14 * i
        pygame.draw.rect(screen, color, (x + 1, offy + 1, 9, 29))

def draw_vu_480(screen, eyesy, offx, offy):
    color = eyesy.LGRAY
    for i in range(0,15) :
        x = offx + 8 * i
        pygame.draw.line(screen, color, [x, offy], [x + 6, offy], 1)
        pygame.draw.line(screen, color, [x, offy], [x, offy + 20], 1)
        pygame.draw.line(screen, color, [x + 6, offy], [x + 6, offy + 20], 1)
        pygame.draw.line(screen, color, [x, offy + 20], [x + 6, offy + 20], 1)
    color = eyesy.GREEN
    for i in range(0, int(eyesy.audio_peak / 2048)):
        if i > 8 : color = (255,255,0)
        if i == 14 : color = eyesy.RED
        x = offx + 8 * i
        if i < 15 : pygame.draw.rect(screen, color, (x + 1, offy + 1, 5, 19))


# loading banner helper
def loading_banner(screen, stuff) :
    screen.fill((0,0,0)) 
        
    font = pygame.font.Font("./font.ttf", 80)
    text = font.render("EYESY", True, (255,255,255))
    textpos = text.get_rect()
    textpos.centerx = screen.get_width() / 2
    textpos.centery = screen.get_height() /2
    screen.blit(text, textpos)

    font = pygame.font.Font("./font.ttf", 16)
    text = font.render(stuff, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.y = screen.get_height() - 100
    screen.blit(text, text_rect)
    pygame.display.flip()

def draw_color_palette(surface, eyesy):
    
    # bg
    width, height = 125, 125  
    xoff = 400
    yoff = 10
    for i in range(height):
        # Get the color using the color_picker function
        color = eyesy.color_picker_bg_preview(i / height)
        # Draw a horizontal line (1 pixel high)
        pygame.draw.line(surface, color, (xoff, i + yoff), (width - 1 + xoff, i + yoff))

    # fg
    width, height = 75, 75  
    xoff = 440
    yoff = 30
    for i in range(height):
        # Get the color using the color_picker function
        color = eyesy.color_picker(i / height)
        # Draw a horizontal line (1 pixel high)
        pygame.draw.line(surface, color, (xoff, i + yoff), (width - 1 + xoff, i + yoff))


def get_local_ip_ifconfig():
    try:
        # Run the `ifconfig` command and get the output
        result = subprocess.run(['ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise Exception(result.stderr.strip())

        # Extract IP addresses using a regex (looks for IPv4 addresses)
        ip_pattern = re.compile(r'inet\s+(\d+\.\d+\.\d+\.\d+)')
        ips = ip_pattern.findall(result.stdout)

        # Exclude 127.0.0.1 (loopback) and return the first match
        for ip in ips:
            if ip != '127.0.0.1':
                return ip
        return "No non-loopback IP found."
    except Exception as e:
        return f"Error: {e}"


def render_overlay_480(screen, eyesy) :

    font = eyesy.font

    #pygame.draw.line(screen, eyesy.LGRAY, [0,480], [720,480], 1)
    #pygame.draw.line(screen, eyesy.LGRAY, [720,480], [720,0], 1)
    draw_color_palette(screen, eyesy)

    # first time through, gather some info
    if eyesy.osd_first :
        eyesy.ip = get_local_ip_ifconfig()
        eyesy.osd_first = False

    # mode
    txt_str = " Mode: (" + str(eyesy.mode_index + 1) +" of "+str(len(eyesy.mode_names)) + ")" + str(eyesy.mode)      
    text = font.render(txt_str, True, eyesy.LGRAY, eyesy.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.centery = 40
    screen.blit(text, text_rect)
     
    # scene
    if eyesy.scene_set :
        scene_str = " Scene: (" + str(eyesy.scene_index + 1) +" of "+str(len(eyesy.scenes)) + ")"
    else:
        scene_str = " Scene: Not Set "
    text = font.render(scene_str, True, eyesy.LGRAY, eyesy.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.centery = 68
    screen.blit(text, text_rect)   

    # res
    reso = eyesy.RESOLUTIONS[eyesy.config["video_resolution"]]["name"]
    message = f"Screen Size {reso} "
    text =          font.render(message, True, eyesy.LGRAY, eyesy.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 200
    text_rect.centery = 68
    screen.blit(text, text_rect)   
 
    # midi notes
    pygame.draw.rect(screen, eyesy.BLACK, (20, 85, 299, 33))
    text = font.render(" MIDI Notes:", True, eyesy.LGRAY, eyesy.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.centery = 101
    screen.blit(text, text_rect)  
    offx = 120
    offy = 89
    for i in range(0, 33):
        pygame.draw.line(screen, eyesy.LGRAY, [(i*6)+offx, offy], [(i*6)+offx, 24+offy], 1)
    for i in range(0, 5):
        pygame.draw.line(screen, eyesy.LGRAY, [offx, (i*6)+offy], [offx + 192, (i*6)+offy], 1)
    for i in range(0,128):
        if (eyesy.midi_notes[i] > 0):
            pygame.draw.rect(screen, eyesy.LGRAY, (offx + 6 * (i % 32), offy + 6 * (i / 32), 6, 6))
        
    # trigger
    pygame.draw.rect(screen, eyesy.BLACK, (20, 166, 105, 30))
    pygame.draw.rect(screen, eyesy.LGRAY, (98, 169, 24, 24), 1)
    if eyesy.trig:
        pygame.draw.rect(screen, (255,255,0), (98, 169, 24, 24))
  
    # ip    
    txt_str = f" IP Address:  {eyesy.ip} "
    text = font.render(txt_str, True, eyesy.LGRAY, eyesy.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.centery = 150
    screen.blit(text, text_rect)
    

    draw_vu_480(screen, eyesy, 115, 210)

    '''            
    # knobs
    pygame.draw.rect(screen, eyesy.BLACK, (20, 124, 144, 35))
    text = font.render(" Knobs:", True, eyesy.LGRAY, eyesy.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.centery = 141
    screen.blit(text, text_rect)
    draw_knob_slider_480(screen, eyesy, 85, 128, 0)
    draw_knob_slider_480(screen, eyesy, 100, 128, 1)
    draw_knob_slider_480(screen, eyesy, 115, 128, 2)
    draw_knob_slider_480(screen, eyesy, 130, 128, 3)
    draw_knob_slider_480(screen, eyesy, 145, 128, 4)
   
    # input level 
    pygame.draw.rect(screen, eyesy.BLACK, (20, 205, 220, 30))
    txt_str = " Input Level:"
    text = font.render(txt_str, True, eyesy.LGRAY, eyesy.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.centery = 220
    screen.blit(text, text_rect)
    draw_vu_480(screen, eyesy, 115, 210)
    
    # Auto Clear   
    if eyesy.auto_clear :
        txt_str = " Persist: No " 
    else :
        txt_str = " Persist: Yes "         
    text = font.render(txt_str, True, eyesy.LGRAY, eyesy.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.centery = 252
    screen.blit(text, text_rect)
    
    # mem
    txt_str = " Memory Used:  "   + str(int(eyesy.memory_used) + 1) + "% "
    text = font.render(txt_str, True, eyesy.LGRAY, eyesy.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.centery = 306
    screen.blit(text, text_rect)
 
    # midi usb dev
#    if (eyesy.usb_midi_present) :
#        txt_str = " USB MIDI:  "   + str(eyesy.usb_midi_name) + " "
#    else :
#        txt_str = " USB MIDI:  None "
#    text = font.render(txt_str, True, eyesy.LGRAY, eyesy.BLACK)
#    text_rect = text.get_rect()
#    text_rect.x = 20
#    text_rect.centery = 334
#    screen.blit(text, text_rect)
 
    # midi ch
#    txt_str = " MIDI CH:  "   + str(eyesy.midi_ch) + " "
#    text = font.render(txt_str, True, eyesy.LGRAY, eyesy.BLACK)
#    text_rect = text.get_rect()
#    text_rect.x = 20
#    text_rect.centery = 362
#    screen.blit(text, text_rect)
         # SSID    
    txt_str = " Network: FIX ME "
    text = font.render(txt_str, True, eyesy.LGRAY, eyesy.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.centery = 418
    screen.blit(text, text_rect)

    # fps
    txt_str = " FPS:  "   + str(int(eyesy.fps)) + " "
    text = font.render(txt_str, True, eyesy.LGRAY, eyesy.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 10
    text_rect.centery = 10
    screen.blit(text, text_rect)
    
    # version
    txt_str = " v3beta1 "
    text = font.render(txt_str, True, eyesy.LGRAY, eyesy.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.centery = 446
    screen.blit(text, text_rect)
    
    # grabs
    #pygame.draw.rect(screen, eyesy.BLACK, (486, 20, 155, 435))
    #text = font.render(" Recent Grabs", True, eyesy.LGRAY, eyesy.BLACK)
    #text_rect = text.get_rect()
    #text_rect.x = 500
    #text_rect.centery = 37
    #screen.blit(text, text_rect)
    #screen.blit(eyesy.tengrabs_thumbs[0], (500, 78 * 0 + 50))
    #screen.blit(eyesy.tengrabs_thumbs[1], (500, 78 * 1 + 50))
    #screen.blit(eyesy.tengrabs_thumbs[2], (500, 78 * 2 + 50))
    #screen.blit(eyesy.tengrabs_thumbs[3], (500, 78 * 3 + 50))
    #screen.blit(eyesy.tengrabs_thumbs[4], (500, 78 * 4 + 50))
    
    # osd, errors
    i = 0
    font = pygame.font.Font("font.ttf", 16)
    for errorline in eyesy.error.splitlines() :
        errormsg = font.render(errorline, True, eyesy.LGRAY, eyesy.RED) 
        text_rect.x = 50
        text_rect.y = 60 + (i * 20)
        screen.blit(errormsg, text_rect)
        i += 1
'''

