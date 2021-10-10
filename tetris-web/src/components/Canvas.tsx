import React, { useEffect, useRef } from "react";
import { Colors } from "../types";

interface Props {
  width: number;
  height: number;
  field: Colors[][];
  blockSize: number;
}

export const Canvas: React.FC<Props> = (props: Props) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const { field, blockSize, width, height } = props;

  /**
   * Render loop
   */
  useEffect(() => {
    const canvas = canvasRef.current;
    let animation: any;

    /**
     * Render field of Colors to the canvas
     * @param ctx Canvas context
     */
    const draw = (ctx: any) => {
      ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
      ctx.fillStyle = "#0d1a48";

      for (let x = 0; x < field[0].length; x++) {
        for (let y = 0; y < field.length; y++) {
          if (field[y][x] === Colors.EMPTY) continue;

          const LINE_WIDTH = 3;
          ctx.strokeStyle = "#0d1a48";
          ctx.lineWidth = LINE_WIDTH;

          switch (field[y][x]) {
            case Colors.ORANGE:
              ctx.fillStyle = "#e56d23";
              break;
            case Colors.GREEN:
              ctx.fillStyle = "#16cc40";
              break;
            case Colors.RED:
              ctx.fillStyle = "#d23542";
              break;
            case Colors.YELLOW:
              ctx.fillStyle = "#f7ca18";
              break;
            case Colors.BLUE:
              ctx.fillStyle = "#4a68dd";
              break;
            case Colors.CYAN:
              ctx.fillStyle = "#5cddd7";
              break;
            case Colors.PURPLE:
              ctx.fillStyle = "#960ac3";
              break;
            default:
              ctx.fillStyle = "#898989";
              break;
          }

          ctx.fillRect(x * blockSize, y * blockSize, blockSize, blockSize);
          ctx.strokeRect(x * blockSize, y * blockSize, blockSize, blockSize);
        }
      }
    };

    if (canvas) {
      const ctx = canvas.getContext("2d");
      if (ctx) draw(ctx);
    }

    return () => {
      window.cancelAnimationFrame(animation);
    };
  }, [field, blockSize]);

  return (
    <canvas
      ref={canvasRef}
      width={width}
      height={height}
      style={{ backgroundColor: "#0d1a48" }}
    />
  );
};
