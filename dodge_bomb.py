import os
import sys
import pygame as pg
import random
import time
WIDTH, HEIGHT = 1100, 650
DELTA = { # 押下キーと移動量の対応表
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:  # 横方向判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate
def gameover(screen: pg.Surface) -> None:
    """
    引数：画面Surface
    戻り値：なし
    画面をブラックアウトし，泣いているこうかとんと
    「Game Over」の文字を5秒間表示する
    """
    bo_img = pg.Surface((WIDTH, HEIGHT))  # 黒い画面用の空Surface
    pg.draw.rect(bo_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    bo_img.set_alpha(200)  # 半透明にする

    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))  # 白文字
    txt_rct = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    bo_img.blit(txt, txt_rct)

    cry_img = pg.image.load("fig/8.png")  # 泣いているこうかとん
    bo_img.blit(cry_img, cry_img.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2)))
    bo_img.blit(cry_img, cry_img.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2)))

    screen.blit(bo_img, [0, 0])
    pg.display.update()
    time.sleep(5)
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) # 爆弾用の空Surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) # 赤い半径10の円 
    bb_img.set_colorkey((0, 0, 0))  # 黒い部分を透明にする
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(10, WIDTH - 10)
    bb_rct.centery = random.randint(10, HEIGHT - 10)
    vx, vy = +5, +5  # 爆弾速度ベクトル
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True): 
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出たら反転
            vx *= -1
        if not tate:  # 縦方向にはみ出たら反転
            vy *= -1
        screen.blit(bb_img, bb_rct)
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()