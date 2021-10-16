import { Block, Colors } from "../types";
import { shapeToCoordinates } from "./shapes";

/**
 * Evaluates if a shape is colliding with the or another shape.
 * @param x         The x coordinate of the shape.
 * @param y         The y coordinate of the shape.
 * @param shape     The shape to evaluate.
 * @param field     The field to evaluate against.
 * @param rotation  The rotation of the shape.
 * @returns         Object with the following properties:
 *                      - outOfBounds: Shape will leave the bounds of the field.
 *                      - collision: Shape collides with another shape or the bottom.
 *                      - combined: Combined boolean of the both properties.
 */
export const evalCollision = (
  player: Block,
  field: Colors[][],
  xOffset: number,
  yOffset: number,
  rotation?: number
) => {
  const coordinates = shapeToCoordinates(
    player.x + xOffset,
    player.y + yOffset,
    player.shape,
    rotation || player.rotation
  );

  const outOfBoundsTop = coordinates.some(({ x, y }) => {
    return y < 0;
  });

  const outOfBoundsLeft = coordinates.some(({ x, y }) => {
    return x < 0;
  });

  const outOfBoundsRight = coordinates.some(({ x, y }) => {
    return x > field[0].length - 1;
  });

  const outOfBoundsBottom = coordinates.some(({ x, y }) => {
    return y > field.length - 1;
  });

  const outOfBounds =
    outOfBoundsTop || outOfBoundsLeft || outOfBoundsRight || outOfBoundsBottom;

  if (!outOfBounds) {
    let collision = coordinates.some(
      ({ x, y }) => field[y][x] !== Colors.EMPTY
    );

    collision = collision || coordinates.some(({ x, y }) => y >= field.length);

    return {
      outOfBounds: {
        top: outOfBoundsTop,
        left: outOfBoundsLeft,
        right: outOfBoundsRight,
        bottom: outOfBoundsBottom,
      },
      collision,
      combined: outOfBounds || collision,
    };
  }

  return {
    outOfBounds: {
      top: outOfBoundsTop,
      left: outOfBoundsLeft,
      right: outOfBoundsRight,
      bottom: outOfBoundsBottom,
    },
    collision: false || coordinates.some(({ x, y }) => y >= field.length),
    combined: true,
  };
};
