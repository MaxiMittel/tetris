import { Block, Colors, Rotation, Shape } from "../types";

/**
 * Draws a T-shape.
 * @param x x-coordinate of the top-left corner of the shape.
 * @param y y-coordinate of the top-left corner of the shape.
 * @param rotation Rotation of the shape.
 * @returns Array of coordinates of the shape.
 */
export const TShape = (x: number, y: number, rotation: Rotation) => {
  switch (rotation) {
    case Rotation.UP:
      return [
        { x: x, y: y },
        { x: x + 1, y: y },
        { x: x + 2, y: y },
        { x: x + 1, y: y + 1 },
      ];
    case Rotation.RIGHT:
      return [
        { x: x, y: y },
        { x: x, y: y + 1 },
        { x: x, y: y + 2 },
        { x: x + 1, y: y + 1 },
      ];
    case Rotation.DOWN:
      return [
        { x: x, y: y + 1 },
        { x: x + 1, y: y + 1 },
        { x: x + 2, y: y + 1 },
        { x: x + 1, y: y },
      ];
    case Rotation.LEFT:
      return [
        { x: x + 1, y: y },
        { x: x + 1, y: y + 1 },
        { x: x + 1, y: y + 2 },
        { x: x, y: y + 1 },
      ];
  }
};

/**
 * Draws a L-shape.
 * @param x x-coordinate of the top-left corner of the shape.
 * @param y y-coordinate of the top-left corner of the shape.
 * @param rotation Rotation of the shape.
 * @returns Array of coordinates of the shape.
 */
export const LShape = (x: number, y: number, rotation: Rotation) => {
  switch (rotation) {
    case Rotation.UP:
      return [
        { x: x, y: y },
        { x: x, y: y + 1 },
        { x: x + 1, y: y + 1 },
        { x: x + 2, y: y + 1 },
      ];
    case Rotation.RIGHT:
      return [
        { x: x, y: y },
        { x: x + 1, y: y },
        { x: x, y: y + 1 },
        { x: x, y: y + 2 },
      ];
    case Rotation.DOWN:
      return [
        { x: x, y: y },
        { x: x + 1, y: y },
        { x: x + 2, y: y },
        { x: x + 2, y: y + 1 },
      ];
    case Rotation.LEFT:
      return [
        { x: x + 1, y: y },
        { x: x + 1, y: y + 1 },
        { x: x + 1, y: y + 2 },
        { x: x, y: y + 2 },
      ];
  }
};

/**
 * Draws a Z-shape.
 * @param x x-coordinate of the top-left corner of the shape.
 * @param y y-coordinate of the top-left corner of the shape.
 * @param rotation Rotation of the shape.
 * @returns Array of coordinates of the shape.
 */
export const ZShape = (x: number, y: number, rotation: Rotation) => {
  switch (rotation) {
    case Rotation.UP:
      return [
        { x: x + 1, y: y },
        { x: x, y: y + 1 },
        { x: x + 1, y: y + 1 },
        { x: x, y: y + 2 },
      ];
    case Rotation.RIGHT:
      return [
        { x: x + 1, y: y },
        { x: x, y: y },
        { x: x + 1, y: y + 1 },
        { x: x + 2, y: y + 1 },
      ];
    case Rotation.DOWN:
      return [
        { x: x, y: y },
        { x: x, y: y + 1 },
        { x: x + 1, y: y + 1 },
        { x: x + 1, y: y + 2 },
      ];
    case Rotation.LEFT:
      return [
        { x: x + 1, y: y },
        { x: x, y: y + 1 },
        { x: x + 1, y: y + 1 },
        { x: x + 2, y: y },
      ];
  }
};

/**
 * Draws an Bar-shape.
 * @param x x-coordinate of the top-left corner of the shape.
 * @param y y-coordinate of the top-left corner of the shape.
 * @param rotation Rotation of the shape.
 * @returns Array of coordinates of the shape.
 */
export const BarShape = (x: number, y: number, rotation: Rotation) => {
  switch (rotation) {
    case Rotation.UP:
    case Rotation.DOWN:
      return [
        { x: x, y: y },
        { x: x + 1, y: y },
        { x: x + 2, y: y },
        { x: x + 3, y: y },
      ];
    case Rotation.RIGHT:
    case Rotation.LEFT:
      return [
        { x: x, y: y },
        { x: x, y: y + 1 },
        { x: x, y: y + 2 },
        { x: x, y: y + 3 },
      ];
  }
};

/**
 * Draws a Block-shape.
 * @param x x-coordinate of the top-left corner of the shape.
 * @param y y-coordinate of the top-left corner of the shape.
 * @param rotation Rotation of the shape.
 * @returns Array of coordinates of the shape.
 */
export const BlockShape = (x: number, y: number, rotation: Rotation) => {
  return [
    { x: x, y: y },
    { x: x, y: y + 1 },
    { x: x + 1, y: y },
    { x: x + 1, y: y + 1 },
  ];
};

/**
 * Will return the coordinates of the shape provided in the parameter.
 * @param x x-coordinate of the top-left corner of the shape.
 * @param y y-coordinate of the top-left corner of the shape.
 * @param shape The requested shape.
 * @param rotation Rotation of the shape.
 * @returns Array of coordinates of the shape.
 */
export const shapeToCoordinates = (
  x: number,
  y: number,
  shape: Shape,
  rotation: Rotation
) => {
  switch (shape) {
    case Shape.T:
      return TShape(x, y, rotation);
    case Shape.L:
      return LShape(x, y, rotation);
    case Shape.Z:
      return ZShape(x, y, rotation);
    case Shape.BAR:
      return BarShape(x, y, rotation);
    case Shape.BLOCK:
      return BlockShape(x, y, rotation);
    default:
      return [];
  }
};

/**
 * Draws a shape onto a field of Colors.
 * @param field     The field to draw the shape on.
 * @param x         x-coordinate of the top-left corner of the shape.
 * @param y         y-coordinate of the top-left corner of the shape.
 * @param color     Color of the shape.
 * @param shape     The shape to draw.
 * @param rotation  Rotation of the shape.
 * @returns         A copy of the field with the shape drawn on it.
 */
export const drawShape = (player: Block, field: Colors[][]) => {
  let shapeToDraw: { x: number; y: number }[] = shapeToCoordinates(
    player.x,
    player.y,
    player.shape,
    player.rotation
  );

  let fieldCopy = field.map(function (arr) {
    return arr.slice();
  });

  shapeToDraw.forEach(({ x, y }) => {
    fieldCopy[y][x] = player.color;
  });

  return fieldCopy;
};
