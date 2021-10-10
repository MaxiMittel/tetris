import React, { useCallback, useEffect, useRef } from "react";
import { Colors } from "../types";

interface Props {
    width: number;
    height: number;
    field: Colors[][];
    blockSize: number;
}

export const Canvas: React.FC<Props> = (props: Props) => {

    const canvasRef = useRef<HTMLCanvasElement | null>(null);

    /**
     * Render field of Colors to the canvas
     * @param ctx Canvas context
     */
    const draw = useCallback((ctx: any) => {
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height)
        ctx.fillStyle = '#000000'

        for (let x = 0; x < props.field[0].length; x++) {
            for (let y = 0; y < props.field.length; y++) {

                if(props.field[y][x] === Colors.EMPTY) continue;

                const LINE_WIDTH = 3;
                ctx.strokeStyle = "#ffffff";
                ctx.lineWidth = LINE_WIDTH;

                switch (props.field[y][x]) {
                    case Colors.BLUE:
                        ctx.fillStyle= "#00CAE0";
                        break;
                    case Colors.GREEN:
                        ctx.fillStyle= "#28E247";
                        break;
                    case Colors.RED:
                        ctx.fillStyle= "#FF500A";
                        break;
                    case Colors.YELLOW:
                        ctx.fillStyle= "#FECB34";
                        break;
                }

                ctx.fillRect(x * props.blockSize, y * props.blockSize, props.blockSize, props.blockSize);
                ctx.strokeRect(x * props.blockSize, y * props.blockSize, props.blockSize, props.blockSize);
            }
        }
      }, [props.field, props.blockSize]);
      
      /**
       * Render loop
       */
      useEffect(() => {
        const canvas = canvasRef.current;
        let animation: any;

        if(canvas){
            const ctx = canvas.getContext('2d')
            if(ctx){
                const loop = () => {
                    draw(ctx)
                    animation = requestAnimationFrame(loop)
                }
                loop()
            }
        }
        
        return () => {
          window.cancelAnimationFrame(animation)
        }
      }, [draw])
  

  return <canvas ref={canvasRef} width={props.width} height={props.height} style={{backgroundColor: "black"}}/>;
};


