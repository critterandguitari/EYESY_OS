import pygame
import socket

etc = None

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

# loading banner helper
def loading_banner(screen, stuff) :
    global etc
    screen.fill((0,0,0)) 
        
    font = pygame.font.Font("./font.ttf", 150)
    text = font.render("EYESY", True, (255,255,255))
    textpos = text.get_rect()
    textpos.centerx = screen.get_width() / 2
    textpos.centery = screen.get_height() /2
    screen.blit(text, textpos)

    font = pygame.font.Font("./font.ttf", 32)
    text = font.render(stuff, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.x = 20
    text_rect.y = 650
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
        mode_str = " Clear BG: Yes " 
    else :
        mode_str = " Clear BG: No "         
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
   # mode_str = " FPS:  "   + str(int(etc.fps)) + " "
   # text = font.render(mode_str, True, etc.WHITE, etc.BLACK)
   # text_rect = text.get_rect()
   # text_rect.x = 790
   # text_rect.centery = 588
   # screen.blit(text, text_rect)
    
    # version
    mode_str = " v1.0 "
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


