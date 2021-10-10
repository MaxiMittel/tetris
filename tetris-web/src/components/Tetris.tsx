import React, { useCallback, useEffect, useRef, useState } from "react";
import { evalCollision } from "../tetris/collision";
import { drawShape } from "../tetris/shapes";
import { Block, Colors, Rotation, Shape } from "../types";
import { Canvas } from "./Canvas";

interface Props {
  field: Colors[][];
  player: Block;
  onPlayerMove: (player: Block) => void;
  onBlockFix: (field: Colors[][]) => void;
}

export const Tetris: React.FC<Props> = (props: Props) => {
  const block_size = 25;
  const [gamefieldDisplay, setGameFieldDisplay] = React.useState(props.field);
  const fixPositionTimer = useRef<any>();
  const [fixed, setFixed] = useState(false);

  const { field, player, onBlockFix, onPlayerMove } = props;

  /**
   * Draw the player shape on the gamefield
   */
  useEffect(() => {
    setGameFieldDisplay(drawShape(player, field));
  }, [player, field]);

  /**
   * Check if the player collided with other Colors or the bottom of the gamefield
   */
  useEffect(() => {
    const collisionBelow = evalCollision(player, field, 0, 1);

    if (collisionBelow.collision) {
      setFixed(true);
      clearTimeout(fixPositionTimer.current);
      fixPositionTimer.current = setTimeout(() => {
        onBlockFix(drawShape(player, field));
        setFixed(false);
      }, 1000);
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

          const collision = evalCollision(player, field, 0, 1);

          if (!collision.combined && !fixed) {
            onPlayerMove({ ...player, y: player.y + 1 });
          }

          break;
        case "ArrowLeft":
          event.preventDefault();
          if (!evalCollision(player, field, -1, 0).combined) {
            onPlayerMove({ ...player, x: player.x - 1 });
          }
          break;
        case "ArrowRight":
          event.preventDefault();
          if (!evalCollision(player, field, 1, 0).combined) {
            onPlayerMove({ ...player, x: player.x + 1 });
          }
          break;
        case "ArrowUp":
          event.preventDefault();
          onPlayerMove({ ...player, rotation: (player.rotation + 1) % 4 });
          break;
      }
    },
    [field, fixed, player, onPlayerMove]
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
    />
  );
};
