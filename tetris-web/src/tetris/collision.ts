import { Block, Colors, Rotation, Shape } from "../types";
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
export const evalCollision = (player: Block, field: Colors[][], xOffset: number, yOffset: number) => {
  const coordinates = shapeToCoordinates(
    player.x + xOffset,
    player.y + yOffset,
    player.shape,
    player.rotation
  );

  const outOfBounds = coordinates.some(({ x, y }) => {
    return y < 0 || y >= field.length || x < 0 || x >= field[0].length;
  });

  if (!outOfBounds) {
    let collision = coordinates.some(
      ({ x, y }) => field[y][x] !== Colors.EMPTY
    );

    collision = collision || coordinates.some(({ x, y }) => y >= field.length);

    return {
      outOfBounds,
      collision,
      combined: outOfBounds || collision,
    };
  }

  return {
    outOfBounds,
    collision: false || coordinates.some(({ x, y }) => y >= field.length),
    combined: true,
  };
};
