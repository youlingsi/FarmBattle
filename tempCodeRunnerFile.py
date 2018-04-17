        for tile in gm.map:
            if gm.map[tile] == 1:
                screen.blit(field, gm.indexToPos(tile))
            else:
                screen.blit(grass, gm.indexToPos(tile))