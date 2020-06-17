import pygame
import socket
import imp

etc = None

wifi = imp.load_source('wifi_control', '/home/music/EYESY_OS/system/wifi_control.py')

def init(etc_obj) :
    global etc
    etc = etc_obj

def draw_knob_slider(screen, etc, offx, offy, index) :
    if etc.knob_override[index]:
        color = etc.RED
    else :
        color = etc.WHITE
    pygame.draw.line(screen, color, [offx, offy], [offx + 16, offy], 1)
    pygame.draw.line(screen, color, [offx, offy], [offx, offy + 40], 1)
    pygame.draw.line(screen, color, [offx + 16, offy], [offx + 16, offy + 40], 1)
    pygame.draw.line(screen, color, [offx, offy + 40], [offx + 16, offy + 40], 1)
    pygame.draw.rect(screen, color, (offx, offy + 40 - int(40*etc.knob[index]), 16, int(40*etc.knob[index])))

def draw_knob_slider_480(screen, etc, offx, offy, index) :
    if etc.knob_override[index]:
        color = etc.RED
    else :
        color = etc.WHITE
    pygame.draw.line(screen, color, [offx, offy], [offx + 10, offy], 1)
    pygame.draw.line(screen, color, [offx, offy], [offx, offy + 24], 1)
    pygame.draw.line(screen, color, [offx + 10, offy], [offx + 10, offy + 24], 1)
    pygame.draw.line(screen, color, [offx, offy + 24], [offx + 10, offy + 24], 1)
    pygame.draw.rect(screen, color, (offx, offy + 24 - int(24*etc.knob[index]), 10, int(24*etc.knob[index])))


def draw_vu(screen, etc, offx, offy):
    color = etc.WHITE
    for i in range(0,15) :
        x = offx + 14 * i
        pygame.draw.line(screen, color, [x, offy], [x + 10, offy], 1)
        pygame.draw.line(screen, color, [x, offy], [x, offy + 30], 1)
        pygame.draw.line(screen, color, [x + 10, offy], [x + 10, offy + 30], 1)
        pygame.draw.line(screen, color, [x, offy + 30], [x + 10, offy + 30], 1)
    color = etc.GREEN
    for i in range(0, etc.audio_peak / 2048):
        if i > 8 : color = (255,255,0)
        if i == 14 : color = etc.RED
        x = offx + 14 * i
        pygame.draw.rect(screen, color, (x + 1, offy + 1, 9, 29))

def draw_vu_480(screen, etc, offx, offy):
    color = etc.WHITE
    for i in range(0,15) :
        x = offx + 8 * i
        pygame.draw.line(screen, color, [x, offy], [x + 6, offy], 1)
        pygame.draw.line(screen, color, [x, offy], [x, offy + 20], 1)
        pygame.draw.line(screen, color, [x + 6, offy], [x + 6, offy + 20], 1)
        pygame.draw.line(screen, color, [x, offy + 20], [x + 6, offy + 20], 1)
    color = etc.GREEN
    for i in range(0, etc.audio_peak / 2048):
        if i > 8 : color = (255,255,0)
        if i == 14 : color = etc.RED
        x = offx + 8 * i
        if i < 15 : pygame.draw.rect(screen, color, (x + 1, offy + 1, 5, 19))


# loading banner helper
def loading_banner(screen, stuff) :
    global etc
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

# main screen osd
def render_overlay(screen) :
    global etc

    font = pygame.font.Font("font.ttf", 32)

    # first time through, gather some info
    if etc.osd_first :
        etc.ip = socket.gethostbyname(socket.gethostname())
        etc.osd_first = False

    # mode
    mode_str = " Mode:  "   + str(etc.mode) + " (" + str(etc.mode_index + 1) +" of "+str(len(etc.mode_names)) + ")"
    text = font.render(mode_str, True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 50
    text_rect.centery = 200
    screen.blit(text, text_rect)
    
    # scene
    if etc.scene_set :
        scene_str = " Scene:  " + str(etc.scene_index + 1) +" of "+str(len(etc.scenes)) + " "
    else:
        scene_str = " Scene: Not Set "
    text = font.render(scene_str, True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 50
    text_rect.centery = 253
    screen.blit(text, text_rect)   
    
    # midi notes
    pygame.draw.rect(screen, etc.BLACK, (50, 285, 530, 55))
    text = font.render(" MIDI Notes:", True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 50
    text_rect.centery = 314
    screen.blit(text, text_rect)  
    offx = 250
    offy = 292
    for i in range(0, 33):
        pygame.draw.line(screen, etc.WHITE, [(i*10)+offx, offy], [(i*10)+offx, 40+offy], 1)
    for i in range(0, 5):
        pygame.draw.line(screen, etc.WHITE, [offx, (i*10)+offy], [offx + 320, (i*10)+offy], 1)
    for i in range(0,128):
        if (etc.midi_notes[i] > 0):
            pygame.draw.rect(screen, etc.WHITE, (offx + 10 * (i % 32), offy + 10 * (i / 32), 10, 10))
            
    # knobs
    pygame.draw.rect(screen, etc.BLACK, (50, 355, 228, 55))
    text = font.render(" Knobs:", True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 50
    text_rect.centery = 385
    screen.blit(text, text_rect)
    draw_knob_slider(screen, etc, 170, 362, 0)
    draw_knob_slider(screen, etc, 190, 362, 1)
    draw_knob_slider(screen, etc, 210, 362, 2)
    draw_knob_slider(screen, etc, 230, 362, 3)
    draw_knob_slider(screen, etc, 250, 362, 4)
    
    # trigger
    pygame.draw.rect(screen, etc.BLACK, (50, 420, 175, 45))
    text = font.render(" Trigger:", True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 50
    text_rect.centery = 440
    screen.blit(text, text_rect)
    pygame.draw.rect(screen, etc.WHITE, (180, 425, 40, 35), 1)
    if etc.audio_trig:
        pygame.draw.rect(screen, (255,255,0), (180, 425, 40, 35))
    
    # input level 
    mode_str = " Input Level:                         "
    text = font.render(mode_str, True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 50
    text_rect.centery = 500
    screen.blit(text, text_rect)
    draw_vu(screen, etc, 240, 484)
    
    # Auto Clear   
    if etc.auto_clear :
        mode_str = " Persist: No " 
    else :
        mode_str = " Persist: Yes "         
    text = font.render(mode_str, True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 50
    text_rect.centery = 555
    screen.blit(text, text_rect)
    
    # ip    
    mode_str = " IP Address:  "   + str(etc.ip) + " "
    text = font.render(mode_str, True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 790
    text_rect.centery = 480
    screen.blit(text, text_rect)
    
    # mem
    mode_str = " Memory Used:  "   + str(int(etc.memory_used) + 1) + "% "
    text = font.render(mode_str, True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 790
    text_rect.centery = 535
    screen.blit(text, text_rect)
 
    # midi usb dev
    if (etc.usb_midi_present) :
        mode_str = " USB MIDI:  "   + str(etc.usb_midi_name) + " "
    else :
        mode_str = " USB MIDI:  None "
    text = font.render(mode_str, True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 790
    text_rect.centery = 588
    screen.blit(text, text_rect)
 
    # midi ch
    mode_str = " MIDI CH:  "   + str(etc.midi_ch) + " "
    text = font.render(mode_str, True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 790
    text_rect.centery = 643
    screen.blit(text, text_rect)
    
    # fps
    mode_str = " FPS:  "   + str(int(etc.fps)) + " "
    text = font.render(mode_str, True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 10
    text_rect.centery = 10
    screen.blit(text, text_rect)
    
    # version
    mode_str = " v1.1 "
    text = font.render(mode_str, True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 1180
    text_rect.centery = 680
    screen.blit(text, text_rect)
    
    # grabs
    pygame.draw.rect(screen, etc.BLACK, (790, 150, 418, 295))
    text = font.render(" Recent Grabs", True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 790
    text_rect.centery = 175
    screen.blit(text, text_rect)
    for i in range(0,3) :
        screen.blit(etc.tengrabs_thumbs[i], (135 * i + 800,200))
    for i in range(0,3) :
        screen.blit(etc.tengrabs_thumbs[i + 3], (135 * i + 800,280))
    for i in range(0,3) :
        screen.blit(etc.tengrabs_thumbs[i + 6], (135 * i + 800,360))
   

    # osd, errors
    i = 0
    font = pygame.font.Font("font.ttf", 24)
    for errorline in etc.error.splitlines() :
        errormsg = font.render(errorline, True, etc.WHITE, etc.RED) 
        text_rect.x = 50
        text_rect.y = 100 + (i * 32)
        screen.blit(errormsg, text_rect)
        i += 1

def render_overlay_480(screen) :
    global etc

    font = pygame.font.Font("font.ttf", 16)

    #pygame.draw.line(screen, etc.WHITE, [0,480], [720,480], 1)
    #pygame.draw.line(screen, etc.WHITE, [720,480], [720,0], 1)
    
    # first time through, gather some info
    if etc.osd_first :
        etc.ip = socket.gethostbyname(socket.gethostname())
        wifi.wifi_connected() # get the ip and ssid
        etc.osd_first = False

    # mode
    mode_str = " Mode:  "   + str(etc.mode) + " (" + str(etc.mode_index + 1) +" of "+str(len(etc.mode_names)) + ")"
    text = font.render(mode_str, True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.centery = 40
    screen.blit(text, text_rect)
    
    # scene
    if etc.scene_set :
        scene_str = " Scene:  " + str(etc.scene_index + 1) +" of "+str(len(etc.scenes)) + " "
    else:
        scene_str = " Scene: Not Set "
    text = font.render(scene_str, True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.centery = 68
    screen.blit(text, text_rect)   
    
    # midi notes
    pygame.draw.rect(screen, etc.BLACK, (20, 85, 299, 33))
    text = font.render(" MIDI Notes:", True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.centery = 101
    screen.blit(text, text_rect)  
    offx = 120
    offy = 89
    for i in range(0, 33):
        pygame.draw.line(screen, etc.WHITE, [(i*6)+offx, offy], [(i*6)+offx, 24+offy], 1)
    for i in range(0, 5):
        pygame.draw.line(screen, etc.WHITE, [offx, (i*6)+offy], [offx + 192, (i*6)+offy], 1)
    for i in range(0,128):
        if (etc.midi_notes[i] > 0):
            pygame.draw.rect(screen, etc.WHITE, (offx + 6 * (i % 32), offy + 6 * (i / 32), 6, 6))
            
    # knobs
    pygame.draw.rect(screen, etc.BLACK, (20, 124, 144, 35))
    text = font.render(" Knobs:", True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.centery = 141
    screen.blit(text, text_rect)
    draw_knob_slider_480(screen, etc, 85, 128, 0)
    draw_knob_slider_480(screen, etc, 100, 128, 1)
    draw_knob_slider_480(screen, etc, 115, 128, 2)
    draw_knob_slider_480(screen, etc, 130, 128, 3)
    draw_knob_slider_480(screen, etc, 145, 128, 4)
    
    # trigger
    pygame.draw.rect(screen, etc.BLACK, (20, 166, 105, 30))
    text = font.render(" Trigger:", True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.centery = 180
    screen.blit(text, text_rect)
    pygame.draw.rect(screen, etc.WHITE, (98, 169, 24, 24), 1)
    if etc.audio_trig:
        pygame.draw.rect(screen, (255,255,0), (98, 169, 24, 24))
    
    # input level 
    pygame.draw.rect(screen, etc.BLACK, (20, 205, 220, 30))
    mode_str = " Input Level:"
    text = font.render(mode_str, True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.centery = 220
    screen.blit(text, text_rect)
    draw_vu_480(screen, etc, 115, 210)
    
    # Auto Clear   
    if etc.auto_clear :
        mode_str = " Persist: No " 
    else :
        mode_str = " Persist: Yes "         
    text = font.render(mode_str, True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.centery = 252
    screen.blit(text, text_rect)
    
    # mem
    mode_str = " Memory Used:  "   + str(int(etc.memory_used) + 1) + "% "
    text = font.render(mode_str, True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.centery = 306
    screen.blit(text, text_rect)
 
    # LINK session
    if (etc.link_connected) :
        mode_str = " LINK Connected: Yes "
    else :
        mode_str = " LINK Connected: No "
    text = font.render(mode_str, True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.centery = 334
    screen.blit(text, text_rect)
 
    # midi usb dev
#    if (etc.usb_midi_present) :
#        mode_str = " USB MIDI:  "   + str(etc.usb_midi_name) + " "
#    else :
#        mode_str = " USB MIDI:  None "
#    text = font.render(mode_str, True, etc.WHITE, etc.BLACK)
#    text_rect = text.get_rect()
#    text_rect.x = 20
#    text_rect.centery = 334
#    screen.blit(text, text_rect)
 
    # midi ch
#    mode_str = " MIDI CH:  "   + str(etc.midi_ch) + " "
#    text = font.render(mode_str, True, etc.WHITE, etc.BLACK)
#    text_rect = text.get_rect()
#    text_rect.x = 20
#    text_rect.centery = 362
#    screen.blit(text, text_rect)
      
    # ip    
    mode_str = " IP Address:  "   + wifi.ip_address + " "
    text = font.render(mode_str, True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.centery = 390
    screen.blit(text, text_rect)
    
    # SSID    
    mode_str = " Network:  "   + wifi.current_net + " "
    text = font.render(mode_str, True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.centery = 418
    screen.blit(text, text_rect)

    # fps
    #mode_str = " FPS:  "   + str(int(etc.fps)) + " "
    #text = font.render(mode_str, True, etc.WHITE, etc.BLACK)
    #text_rect = text.get_rect()
    #text_rect.x = 10
    #text_rect.centery = 10
    #screen.blit(text, text_rect)
    
    # version
    #mode_str = " v1.1 "
    #text = font.render(mode_str, True, etc.WHITE, etc.BLACK)
    #text_rect = text.get_rect()
    #text_rect.x = 1180
    #text_rect.centery = 680
    #screen.blit(text, text_rect)
    
    # grabs
    pygame.draw.rect(screen, etc.BLACK, (486, 20, 155, 435))
    text = font.render(" Recent Grabs", True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 500
    text_rect.centery = 37
    screen.blit(text, text_rect)
    screen.blit(etc.tengrabs_thumbs[0], (500, 78 * 0 + 50))
    screen.blit(etc.tengrabs_thumbs[1], (500, 78 * 1 + 50))
    screen.blit(etc.tengrabs_thumbs[2], (500, 78 * 2 + 50))
    screen.blit(etc.tengrabs_thumbs[3], (500, 78 * 3 + 50))
    screen.blit(etc.tengrabs_thumbs[4], (500, 78 * 4 + 50))
    
    # osd, errors
    i = 0
    font = pygame.font.Font("font.ttf", 16)
    for errorline in etc.error.splitlines() :
        errormsg = font.render(errorline, True, etc.WHITE, etc.RED) 
        text_rect.x = 50
        text_rect.y = 60 + (i * 20)
        screen.blit(errormsg, text_rect)
        i += 1

def render_shift_overlay(screen) :
    global etc

    font = pygame.font.Font("font.ttf", 16)

    # shift lines
    text = font.render(etc.shift_line[0], True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 40
    text_rect.centery = 100
    screen.blit(text, text_rect)

    text = font.render(etc.shift_line[1], True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 40
    text_rect.centery = 150
    screen.blit(text, text_rect)
    
    text = font.render(etc.shift_line[2], True, etc.WHITE, etc.BLACK)
    text_rect = text.get_rect()
    text_rect.x = 40
    text_rect.centery = 200
    screen.blit(text, text_rect)

