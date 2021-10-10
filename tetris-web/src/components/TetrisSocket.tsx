import React, { useState } from "react";
import { randomBlock } from "../tetris/blocks";
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

  const [player, setPlayer] = useState<Block>(randomBlock());
  const [field, setField] = useState(fielda);

  const onBlockFix = (newField: Colors[][]) => {
    setField(newField);
    setPlayer(randomBlock());
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
