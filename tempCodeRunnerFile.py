                        if event.key == pygame.ke:
                            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                                if opSce.selectionStage == 0:
                                    opSce.playerRole = (opSce.playerRole + 1)%2
                                elif opSce.selectionStage == 1:
                                    opSce.mAIon = not opSce.mAIOn
                                elif opSce.selectionStage == 2:
                                    opSce.fAIon = not opSce.fAIon
                            if event.key == pygame.K_RETURN:
                                if opSce.selectionStage == 2:
                                    gamestate += 1
                                    opSce.selectionStage = 0
                                else:
                                    opSce.selectionStage += 1
                            elif event.key == pygame.K_ESCAPE and opSce.selectionStage > 0:
                                opSce.selectionStage -= 1
        