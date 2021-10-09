import React, { useCallback, useEffect, useRef, useState } from "react";
import { evalCollision } from "../tetris/collision";
import { drawShape } from "../tetris/shapes";
import { Blocks, Rotation, Shape } from "../types";
import { Canvas } from "./Canvas";

interface Props {
  field: Blocks[][];
  playerPosition: { x: number; y: number };
  playerShape: Shape;
  playerColor: Blocks;
  playerRotation: Rotation;
  onBlockFix: (field: Blocks[][]) => void;
  onPositionChange: (x: number, y: number) => void;
  onRotationChange: (rotation: Rotation) => void;
}

export const Tetris: React.FC<Props> = (props: Props) => {
  const block_size = 25;
  const [gamefieldDisplay, setGameFieldDisplay] = React.useState(props.field);
  const fixPositionTimer = useRef<any>();
  const [fixed, setFixed] = useState(false);

  const {
    field,
    playerPosition,
    playerShape,
    playerColor,
    playerRotation,
    onBlockFix,
    onPositionChange,
    onRotationChange,
  } = props;

  /**
   * Draw the player shape on the gamefield
   */
  useEffect(() => {
    setGameFieldDisplay(
      drawShape(
        field,
        playerPosition.x,
        playerPosition.y,
        playerColor,
        playerShape,
        playerRotation
      )
    );
  }, [playerPosition, field, playerColor, playerShape, playerRotation]);

  /**
   * Check if the player collided with other blocks or the bottom of the gamefield
   */
  useEffect(() => {
    const collisionBelow = evalCollision(
      playerPosition.x,
      playerPosition.y + 1,
      playerShape,
      field,
      playerRotation
    );

    if (collisionBelow.collision) {
      setFixed(true);
      clearTimeout(fixPositionTimer.current);
      fixPositionTimer.current = setTimeout(() => {
        onBlockFix(
          drawShape(
            field,
            playerPosition.x,
            playerPosition.y,
            playerColor,
            playerShape,
            playerRotation
          )
        );
        setFixed(false);
      }, 1000);
    }
  }, [
    playerPosition,
    playerShape,
    field,
    playerRotation,
    playerColor,
    onBlockFix,
  ]);

  /**
   * KeyDown event handler
   * @param event Keyboard event
   */
  const onKeyDownHandler = useCallback(
    (event: any) => {
      switch (event.key) {
        case "ArrowDown":
          event.preventDefault();

          const collision = evalCollision(
            playerPosition.x,
            playerPosition.y + 1,
            playerShape,
            field,
            playerRotation
          );

          if (!collision.combined && !fixed) {
            onPositionChange(playerPosition.x, playerPosition.y + 1);
          }

          break;
        case "ArrowLeft":
          event.preventDefault();
          if (
            !evalCollision(
              playerPosition.x - 1,
              playerPosition.y,
              playerShape,
              field,
              playerRotation
            ).combined
          ) {
            onPositionChange(playerPosition.x - 1, playerPosition.y);
          }
          break;
        case "ArrowRight":
          event.preventDefault();
          if (
            !evalCollision(
              playerPosition.x + 1,
              playerPosition.y,
              playerShape,
              field,
              playerRotation
            ).combined
          ) {
            onPositionChange(playerPosition.x + 1, playerPosition.y);
          }
          break;
        case "ArrowUp":
          event.preventDefault();
          onRotationChange((playerRotation + 1) % 4);
          break;
      }
    },
    [
      field,
      fixed,
      playerPosition,
      playerShape,
      playerRotation,
      onPositionChange,
      onRotationChange,
    ]
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
