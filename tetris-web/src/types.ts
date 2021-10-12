
export type Lobby = {
    name: string,
    players: number,
    code: string
}

export enum Colors {
    EMPTY,
    ORANGE,
    GREEN,
    RED,
    YELLOW,
    BLUE,
    CYAN,
    PURPLE
}

export enum Shape {
    BLOCK,
    BAR,
    Z,
    L,
    T
}

export enum Rotation {
    UP,
    RIGHT,
    DOWN,
    LEFT
}

export type Block = {
    color: Colors,
    shape: Shape,
    rotation: Rotation,
    x: number,
    y: number
}

export type PlayerEntry = {
    id: string;
    username: string;
    block: Block;
  };

export type ChatMessage = {
    id: string;
    message: string;
};