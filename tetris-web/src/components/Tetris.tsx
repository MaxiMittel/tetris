import React, { useCallback, useEffect, useRef } from "react";
import { evalCollision } from "../tetris/collision";
import { drawShape } from "../tetris/shapes";
import { Colors, PlayerEntry } from "../types";
import { Canvas } from "./Canvas";

interface Props {
  field: Colors[][];
  player: PlayerEntry;
  players: PlayerEntry[];
  onPlayerMove: (player: PlayerEntry) => void;
  onBlockFix: (field: Colors[][]) => void;
}

export const Tetris: React.FC<Props> = (props: Props) => {
  const block_size = 25;
  const [gamefieldDisplay, setGameFieldDisplay] = React.useState(props.field);
  const drawInterval = useRef<any>();
  const fixPositionTimer = useRef<any>();
  const lastMoveDown = useRef<number>(Date.now());

  const { field, player, players, onBlockFix, onPlayerMove } = props;

  /**
   * Move player down
   */
  const moveDown = useCallback(() => {
    const collision = evalCollision(player.block, field, 0, 1);

    if (!collision.combined) {
      onPlayerMove({
        ...player,
        block: {
          ...player.block,
          y: player.block.y + 1,
        },
      });
    }
  }, [player, field, onPlayerMove]);

  /**
   * Draw the player shape on the gamefield
   */
  useEffect(() => {
    drawInterval.current = setInterval(async () => {
      //Move a block after one second
      if (Date.now() - lastMoveDown.current > 1000) {
        moveDown();
        lastMoveDown.current = Date.now();
      }

      //Draw all players to the gamefield
      let newField = drawShape(player.block, field);
      for (let i = 0; i < players.length; i++) {
        if (players[i].block) {
          newField = drawShape(players[i].block, newField);
        }
      }
      setGameFieldDisplay(newField);
    }, 20);

    return () => clearInterval(drawInterval.current);
  }, [player, field, players, moveDown]);

  /**
   * Check if the player collided with other Colors or the bottom of the gamefield
   */
  useEffect(() => {
    const collisionBelow = evalCollision(player.block, field, 0, 1);

    if (collisionBelow.collision) {
      clearTimeout(fixPositionTimer.current);
      fixPositionTimer.current = setTimeout(() => {
        onBlockFix(drawShape(player.block, field));
      }, 500);
    }

    return () => clearTimeout(fixPositionTimer.current);
  }, [player, field, onBlockFix]);

  /**
   * KeyDown event handler
   * @param event Keyboard event
   */
  const onKeyDownHandler = useCallback(
    (event: any) => {
      switch (event.key) {
        case "ArrowDown":
          event.preventDefault();

          const collision = evalCollision(player.block, field, 0, 1);

          if (!collision.combined) {
            onPlayerMove({
              ...player,
              block: { ...player.block, y: player.block.y + 1 },
            });
          }

          break;
        case "ArrowLeft":
          event.preventDefault();
          if (!evalCollision(player.block, field, -1, 0).combined) {
            onPlayerMove({
              ...player,
              block: { ...player.block, x: player.block.x - 1 },
            });
          }
          break;
        case "ArrowRight":
          event.preventDefault();
          if (!evalCollision(player.block, field, 1, 0).combined) {
            onPlayerMove({
              ...player,
              block: { ...player.block, x: player.block.x + 1 },
            });
          }
          break;
        case "ArrowUp":
          event.preventDefault();
          let newRotation = (player.block.rotation + 1) % 4;
          let legalPosition = false;
          let yOff = 0;
          let xOff = 0;

          //Try 10 times to get a valid position
          for (let i = 0; i < 10; i++) {
            const collision = evalCollision(
              player.block,
              field,
              xOff,
              yOff,
              newRotation
            );            
            
            if (!collision.combined) {
              legalPosition = true;
              break;
            }

            if (collision.outOfBounds.bottom) yOff--;
            if (collision.outOfBounds.top) yOff++;
            if (collision.outOfBounds.left) xOff++;
            if (collision.outOfBounds.right) xOff--;
          }

          if (legalPosition) {
            onPlayerMove({
              ...player,
              block: {
                ...player.block,
                x: player.block.x + xOff,
                y: player.block.y + yOff,
                rotation: newRotation,
              },
            });
          }
          break;
        case " ":
          //event.preventDefault();
          let yDiff = 0;
          while (!evalCollision(player.block, field, 0, yDiff).combined) {
            yDiff++;
          }
          onPlayerMove({
            ...player,
            block: { ...player.block, y: player.block.y + (yDiff - 1) },
          });
          break;
      }
    },
    [field, player, onPlayerMove]
  );

  /**
   * Regiser keydown event handler
   */
  useEffect(() => {
    window.addEventListener("keydown", onKeyDownHandler);
    // Remove event listeners on cleanup
    return () => {
      window.removeEventListener("keydown", onKeyDownHandler);
    };
  }, [onKeyDownHandler]);

  return (
    <Canvas
      width={field[0].length * block_size}
      height={field.length * block_size}
      field={gamefieldDisplay}
      blockSize={block_size}
      players={[...players, player]}
    />
  );
};
