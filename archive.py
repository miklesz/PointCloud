# # Bloom Intensity
# def inc_bloom():
#     change_bloom(step=+.1)
#
#
# def dec_bloom():
#     change_bloom(step=-.1)


# def change_bloom(step):
#     """Change bloom intensity"""
#     global bloom
#     bloom = round(bloom+step, 1)
#     if bloom < 0.0:
#         bloom = 0.0
#     filters.set_bloom(blend=(0.3, 0.4, 0.3, 1.0),
#                       mintrigger=0.0,
#                       desat=0,
#                       intensity=bloom,
#                       size="large")  # blend=(0.3,0.4,0.3,0.0), (0.0,0.0,0.0,1.0)


# def toggle_render_mode_perspective():
#     """Toggle render mode perspective"""
#     global render_mode_thickness
#     if base.render.get_render_mode_perspective():
#         base.render.set_render_mode_perspective(False, 1)
#         base.render.set_render_mode_thickness(render_mode_thickness)
#     else:
#         base.render.set_render_mode_perspective(True, 1)
#         base.render.set_render_mode_thickness(render_mode_thickness/1000)


# def inc_separation():
#     change_separation(step=+1)
#
#
# def dec_separation():
#     change_separation(step=-1)


# def change_separation(step):
#     """Change cartoon ink separation"""
#     global separation
#     separation += step
#     if separation == 0:
#         separation = 1
#     if cartoon_ink:
#         filters.setCartoonInk(separation=separation)


# def inc_blur_sharpen():
#     change_blur_sharpen(step=+.1)
#
#
# def dec_blur_sharpen():
#     change_blur_sharpen(step=-.1)
#
#
# def change_blur_sharpen(step):
#     """Change blur/sharpen"""
#     global blur_sharpen
#     blur_sharpen = round(blur_sharpen+step, 1)
#     filters.set_blur_sharpen(amount=blur_sharpen)


# Rendering modes
# def inc_render_mode_thickness():
#     change_render_mode_thickness(step=+1)
#
#
# def dec_render_mode_thickness():
#     change_render_mode_thickness(step=-1)
#
#
# def change_render_mode_thickness(step):
#     """Change render mode thickness"""
#     global render_mode_thickness
#     render_mode_thickness += step
#     if render_mode_thickness == 0:
#         render_mode_thickness = 1
#     if base.render.get_render_mode_perspective():
#         base.render.set_render_mode_thickness(render_mode_thickness/1000)
#     else:
#         base.render.set_render_mode_thickness(render_mode_thickness)


        # elif
        #     pass


# Cartoon Ink
# def toggle_cartoon_ink():
#     """Toggle cartoon ink"""
#     global cartoon_ink
#     if cartoon_ink:
#         filters.del_cartoon_ink()
#         cartoon_ink = False
#     else:
#         filters.set_cartoon_ink()   # separation=1)
#         cartoon_ink = True


# set_modes_and_filters({
#     'bloom': True,
#     'bloom_intensity': 0.0,
#     'blur_sharpen': False,
#     'blur_sharpen_amount': 1.0,
#     'cartoon_ink': False,
#     'cartoon_ink_separation': 1,
#     'render_mode_perspective': False,
#     'render_mode_thickness': 1,
# })
# set_modes_and_filters({
#     'bloom': True,
#     'bloom_intensity': 0.0,
#     'blur_sharpen': False,
#     'blur_sharpen_amount': 1.0,
#     'cartoon_ink': False,
#     'cartoon_ink_separation': 1,
#     'render_mode_perspective': False,
#     'render_mode_thickness': 1,
# })
# print(current_modes_and_filters)
# exit()


# global render_mode_thickness
# global cartoon_ink
# global separation
# global blur_sharpen
# global bloom
# render_mode_thickness = 10
# base.render.set_render_mode_thickness(render_mode_thickness)
# cartoon_ink = True
# separation = 1
# filters.set_cartoon_ink(separation=separation)
# blur_sharpen = 1.0
# filters.set_blur_sharpen(amount=blur_sharpen)
# bloom = False
# filters.del_bloom()
# base.render.set_render_mode_perspective(False, 1)

# base.enableParticles()
# # Start of the code from ptf
# p = ParticleEffect()
# # p.loadConfig(Filename('particles/evaporation_point.ptf'))
# # p.loadConfig(Filename('particles/box.ptf'))
# # p.loadConfig(Filename('particles/evaporation_sprite.ptf'))