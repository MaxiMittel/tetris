
export type Lobby = {
    name: string,
    players: number,
    code: string
}

export enum Blocks {
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