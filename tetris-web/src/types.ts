
export type Lobby = {
    name: string,
    players: number,
    code: string
}

export enum Colors {
    EMPTY,
    BLUE,
    RED,
    YELLOW,
    GREEN,
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