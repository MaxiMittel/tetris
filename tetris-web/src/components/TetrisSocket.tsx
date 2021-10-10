import React, { useState } from "react";
import { Block, Colors, Rotation, Shape } from "../types";
import { Tetris } from "./Tetris";

interface Props {}

export const TetrisSocket: React.FC<Props> = (props: Props) => {
  const randInt = (min: number, max: number) => {
    return Math.floor(Math.random() * (max - min + 1) + min);
  };

  let fielda = new Array<Colors[]>(20);

  for (var i = 0; i < fielda.length; i++) {
    fielda[i] = new Array<Colors>(10).fill(Colors.EMPTY);
  }

  const [player, setPlayer] = useState<Block>({
    color: Colors.RED,
    shape: Shape.T,
    rotation: Rotation.UP,
    x: 0,
    y: 0,
  });
  const [field, setField] = useState(fielda);

  const onBlockFix = (newField: Colors[][]) => {
    setField(newField);
    setPlayer({
      color: randInt(1, 4),
      shape: randInt(0, 4),
      rotation: randInt(0, 3),
      x: 0,
      y: 0,
    });
  };

  return (
    <Tetris
      field={field}
      player={player}
      onPlayerMove={(newPlayer: Block) => setPlayer(newPlayer)}
      onBlockFix={onBlockFix}
    ></Tetris>
  );
};
