import React, { useState } from "react";
import { Blocks, Rotation, Shape } from "../types";
import { Tetris } from "./Tetris";

interface Props {}

export const TetrisSocket: React.FC<Props> = (props: Props) => {
  const [playerRotation, setPlayerRotation] = useState<Rotation>(Rotation.UP);
  const [playerShape, setPlayerShape] = useState(Shape.L);
  const [playerColor, setPlayerColor] = useState(Blocks.RED);

  let fielda = new Array<Blocks[]>(20);

  for (var i = 0; i < fielda.length; i++) {
    fielda[i] = new Array<Blocks>(10).fill(Blocks.EMPTY);
  }

  fielda[10][5] = Blocks.RED;

  const [field, setField] = useState(fielda);
  const [playerPosition, setPlayerPosition] = useState<{
    x: number;
    y: number;
  }>({ x: 0, y: 0 });

  const onBlockFix = (newField: Blocks[][]) => {
    setField(newField);
    setPlayerColor(Math.floor(Math.random() * 5) + 1);
    setPlayerShape(Math.floor(Math.random() * 5));
    setPlayerPosition({ x: 0, y: 0 });
  };

  return (
    <Tetris
      field={field}
      playerPosition={playerPosition}
      playerShape={playerShape}
      playerColor={playerColor}
      playerRotation={playerRotation}
      onPositionChange={(x: number, y: number) => setPlayerPosition({ x, y })}
      onRotationChange={(rotation: Rotation) => setPlayerRotation(rotation)}
      onBlockFix={onBlockFix}
    ></Tetris>
  );
};
