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
      ctx.fillStyle = "#000000";

      for (let x = 0; x < field[0].length; x++) {
        for (let y = 0; y < field.length; y++) {
          if (field[y][x] === Colors.EMPTY) continue;

          const LINE_WIDTH = 3;
          ctx.strokeStyle = "#ffffff";
          ctx.lineWidth = LINE_WIDTH;          

          switch (field[y][x]) {
            case Colors.BLUE:
              ctx.fillStyle = "#00CAE0";
              break;
            case Colors.GREEN:
              ctx.fillStyle = "#28E247";
              break;
            case Colors.RED:
              ctx.fillStyle = "#FF500A";
              break;
            case Colors.YELLOW:
              ctx.fillStyle = "#FECB34";
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
      style={{ backgroundColor: "black" }}
    />
  );
};
