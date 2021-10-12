import { Colors, Rotation, Shape } from "../types";

const blockList = [
  {
    color: Colors.PURPLE,
    shape: Shape.T,
    rotation: Rotation.UP,
    x: 0,
    y: 0,
  },
  {
    color: Colors.CYAN,
    shape: Shape.BAR,
    rotation: Rotation.UP,
    x: 0,
    y: 0,
  },
  {
    color: Colors.BLUE,
    shape: Shape.L,
    rotation: Rotation.UP,
    x: 0,
    y: 0,
  },
  {
    color: Colors.ORANGE,
    shape: Shape.L,
    rotation: Rotation.DOWN,
    x: 0,
    y: 0,
  },
  {
    color: Colors.YELLOW,
    shape: Shape.BLOCK,
    rotation: Rotation.UP,
    x: 0,
    y: 0,
  },
  {
    color: Colors.RED,
    shape: Shape.Z,
    rotation: Rotation.UP,
    x: 0,
    y: 0,
  },
  {
    color: Colors.GREEN,
    shape: Shape.Z,
    rotation: Rotation.DOWN,
    x: 0,
    y: 0,
  },
];

export const randomBlock = (x: number) => {
  const index = Math.floor(Math.random() * blockList.length);
  const block = {...blockList[index], x};
  return block;
};
