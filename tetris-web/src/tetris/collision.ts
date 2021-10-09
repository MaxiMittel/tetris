import { Blocks, Rotation, Shape } from "../types";
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
  x: number,
  y: number,
  shape: Shape,
  field: Blocks[][],
  rotation: Rotation
) => {
  const coordinates = shapeToCoordinates(x, y, shape, rotation);

  const outOfBounds = coordinates.some(({ x, y }) => {
    return y < 0 || y >= field.length || x < 0 || x >= field[0].length;
  });

  if (!outOfBounds) {
    let collision = coordinates.some(
      ({ x, y }) => field[y][x] !== Blocks.EMPTY
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
