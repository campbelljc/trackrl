
class PreviewTrack:
    def __init__(self, a, b, c, d, e, f, g):
        self.index = a
        self.x, self.y, self.z = b, c, d
        self.clearanceZ = e
        self.var_08 = f
        self.flags = g

class QuarterTile:
    # e.g. 0b1111 -> takes all four quarters. Each 1 is a different quarter.
    def __init__(self, tileQuarter, zQuarter=None):
        if tileQuarter == 255:
            return
        if zQuarter is None:
            self.tileQuarter = tileQuarter & 0xF
            self.zQuarter = (tileQuarter >> 4) & 0xF
            self._val = tileQuarter
        else:
            self.tileQuarter = tileQuarter
            self.zQuarter = zQuarter
            self._val = tileQuarter | (zQuarter << 4)
        #print(bin(self.tileQuarter), bin(self.zQuarter), bin(self._val))
        assert len(bin(self.tileQuarter)) <= 6
        assert len(bin(self.zQuarter)) <= 6
        assert len(bin(self._val)) <= 10
    def __str__(self):
        return bin(self.tileQuarter)
    def __repr__(self):
        return str(self)
    def Rotate(self, amount):
        assert amount in range(0, 4), f"Cannot rotate quartertile by {amount}."
        if amount == 0:
            return QuarterTile(self.tileQuarter, self.zQuarter) # QuarterTile{ *this };
        elif amount == 1:
            rotVal1 = self._val << 1;
            rotVal2 = rotVal1 >> 4;
            rotVal1 &= 0b11101110;
            rotVal2 &= 0b00010001;
            return QuarterTile(rotVal1 | rotVal2);
        elif amount == 2:
            rotVal1 = self._val << 2;
            rotVal2 = rotVal1 >> 4;
            rotVal1 &= 0b11001100;
            rotVal2 &= 0b00110011;
            return QuarterTile(rotVal1 | rotVal2)
        elif amount == 3:
            rotVal1 = self._val << 3;
            rotVal2 = rotVal1 >> 4;
            rotVal1 &= 0b10001000;
            rotVal2 &= 0b01110111;
            return QuarterTile(rotVal1 | rotVal2)
        else:
            #print("Tried to rotate QuarterTile invalid amount:", amount);
            return QuarterTile(0, 0);

RCT_PREVIEW_TRACK_FLAG_0 = (1 << 0)
RCT_PREVIEW_TRACK_FLAG_1 = (1 << 1)
RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL = (1 << 2)

TRACK_BLOCK_END = PreviewTrack(255, 255, 255, 255, 255, QuarterTile(255, 255), 255)

TrackBlocks000 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks001 = [
    PreviewTrack( 0, 0, 0, 0, 0,QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks002 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks003 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks004 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks005 = [
    PreviewTrack( 0, 0, 0, 0, 64, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks006 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks007 = [
    PreviewTrack( 0, 0, 0, 0, 32, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks008 = [
    PreviewTrack( 0, 0, 0, 0, 32, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks009 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks010 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks011 = [
    PreviewTrack( 0, 0, 0, 0, 64, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks012 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks013 = [
    PreviewTrack( 0, 0, 0, 0, 32, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks014 = [
    PreviewTrack( 0, 0, 0, 0, 32, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks015 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks016 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, -32, 0, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 4, -32, -64, 0, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, -32, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 6, -64, -64, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks017 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b1110, 0 ), 0 ),
    PreviewTrack( 4, -32, 64, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, 32, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 6, -64, 64, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks018 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks019 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks020 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks021 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks022 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, -32, 0, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 4, -32, -64, 0, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, -32, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 6, -64, -64, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks023 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b1110, 0 ), 0 ),
    PreviewTrack( 4, -32, 64, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, 32, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 6, -64, 64, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks024 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks025 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks026 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks027 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks028 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks029 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks030 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks031 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks032 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks033 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks034 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    PreviewTrack( 1, 0, -32, 16, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 16, 16, QuarterTile( 0b0111, 0b0100 ), 0 ),
    PreviewTrack( 3, -32, -32, 24, 16, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 4, -32, -64, 48, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, -32, 32, 16, QuarterTile( 0b0111, 0b0100 ), 0 ),
    PreviewTrack( 6, -64, -64, 48, 16, QuarterTile( 0b1111, 0b0110 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks035 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    PreviewTrack( 1, 0, 32, 16, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 16, 16, QuarterTile( 0b1011, 0b1000 ), 0 ),
    PreviewTrack( 3, -32, 32, 24, 16, QuarterTile( 0b1110, 0 ), 0 ),
    PreviewTrack( 4, -32, 64, 48, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, 32, 32, 16, QuarterTile( 0b1011, 0b1000 ), 0 ),
    PreviewTrack( 6, -64, 64, 48, 16, QuarterTile( 0b1111, 0b1001 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks036 = [
    PreviewTrack( 0, 0, 0, 48, 16, QuarterTile( 0b1111, 0b0011 ), 0 ),
    PreviewTrack( 1, 0, -32, 48, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 32, 16, QuarterTile( 0b0111, 0b0001 ), 0 ),
    PreviewTrack( 3, -32, -32, 24, 16, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 4, -32, -64, 16, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, -32, 16, 16, QuarterTile( 0b0111, 0b0001 ), 0 ),
    PreviewTrack( 6, -64, -64, 0, 16, QuarterTile( 0b1111, 0b1001 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks037 = [
    PreviewTrack( 0, 0, 0, 48, 16, QuarterTile( 0b1111, 0b0011 ), 0 ),
    PreviewTrack( 1, 0, 32, 48, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 32, 16, QuarterTile( 0b1011, 0b0010 ), 0 ),
    PreviewTrack( 3, -32, 32, 24, 16, QuarterTile( 0b1110, 0 ), 0 ),
    PreviewTrack( 4, -32, 64, 16, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, 32, 16, 16, QuarterTile( 0b1011, 0b0010 ), 0 ),
    PreviewTrack( 6, -64, 64, 0, 16, QuarterTile( 0b1111, 0b0110 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks038 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 2, -32, -32, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 3, -64, -32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks039 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 2, -32, 32, 0, 0, QuarterTile( 0b1110, 0 ), 0 ),
    PreviewTrack( 3, -64, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks040 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    PreviewTrack( 1, -32, 0, 16, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    PreviewTrack( 2, -64, 0, 32, 96, QuarterTile( 0b0010, 0 ), 0 ),
    PreviewTrack( 3, -32, 0, 120, 16, QuarterTile( 0b0110, 0 ), 0 ),
    PreviewTrack( 4, -32, -32, 120, 0, QuarterTile( 0b0000, 0 ), 0 ),
    PreviewTrack( 5, 0, 0, 120, 0, QuarterTile( 0b0000, 0 ), 0 ),
    PreviewTrack( 6, 0, -32, 120, 16, QuarterTile( 0b1001, 0 ), 0 ),
    PreviewTrack( 7, 32, -32, 32, 96, QuarterTile( 0b1000, 0 ), 0 ),
    PreviewTrack( 8, 0, -32, 16, 16, QuarterTile( 0b1111, 0b0011 ), 0 ),
    PreviewTrack( 9, -32, -32, 0, 16, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks041 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    PreviewTrack( 1, -32, 0, 16, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    PreviewTrack( 2, -64, 0, 32, 96, QuarterTile( 0b0001, 0 ), 0 ),
    PreviewTrack( 3, -32, 0, 120, 16, QuarterTile( 0b1001, 0 ), 0 ),
    PreviewTrack( 4, -32, 32, 120, 0, QuarterTile( 0b0000, 0 ), 0 ),
    PreviewTrack( 5, 0, 0, 120, 0, QuarterTile( 0b0000, 0 ), 0 ),
    PreviewTrack( 6, 0, 32, 120, 16, QuarterTile( 0b0110, 0 ), 0 ),
    PreviewTrack( 7, 32, 32, 32, 96, QuarterTile( 0b0100, 0 ), 0 ),
    PreviewTrack( 8, 0, 32, 16, 16, QuarterTile( 0b1111, 0b0011 ), 0 ),
    PreviewTrack( 9, -32, 32, 0, 16, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks042 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 1, 0, -32, 0, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b0010, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks043 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b0001, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks044 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 1, 0, -32, 0, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b0010, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks045 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b0001, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks046 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b0111, 0b0100 ), 0 ),
    PreviewTrack( 1, 0, -32, 16, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 16, 0, QuarterTile( 0b0010, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, 16, 16,QuarterTile( 0b0111, 0b0110 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks047 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1011, 0b1000 ), 0 ),
    PreviewTrack( 1, 0, 32, 16, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 16, 0, QuarterTile( 0b0001, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 16, 16,QuarterTile( 0b1011, 0b1001 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks048 = [
    PreviewTrack( 0, 0, 0, 16, 16,QuarterTile( 0b0111, 0b0011 ), 0 ),
    PreviewTrack( 1, 0, -32, 16, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 16, 0, QuarterTile( 0b0010, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, 0, 16, QuarterTile( 0b0111, 0b0001 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks049 = [
    PreviewTrack( 0, 0, 0, 16, 16, QuarterTile( 0b1011, 0b0011 ), 0 ),
    PreviewTrack( 1, 0, 32, 16, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 16, 0, QuarterTile( 0b0001, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 0, 16, QuarterTile( 0b1011, 0b0010 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks050 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks051 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks052 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, 16, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks053 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, 16, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks054 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, -16, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, -16, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks055 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, -16, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, -16, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks056 = [
    PreviewTrack( 0, 0, 0, 0, 32, QuarterTile( 0b1111, 0b1100 ), 0 ),
    PreviewTrack( 1, -32, 0, 16, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    PreviewTrack( 2, -64, 0, 32, 96,QuarterTile( 0b0011, 0 ), 0 ),
    PreviewTrack( 3, -32, 0, 120, 16, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks057 = [
    PreviewTrack( 0, 0, 0, -32, 32, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, -120, 96,QuarterTile( 0b0011, 0 ), 0 ),
    PreviewTrack( 2, 0, 0, -136, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    PreviewTrack( 3, 32, 0, -152, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks058 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 24, 32, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 2, -32, -32, 48, 16, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks059 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 24, 32, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 2, -32, 32, 48, 16, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks060 = [
    PreviewTrack( 0, 0, 0, -32, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, -56, 32, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 2, -32, -32, -80, 16, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks061 = [
    PreviewTrack( 0, 0, 0, -32, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, -56, 32, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 2, -32, 32, -80, 16, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks062 = [
    PreviewTrack( 0, 0, 0, 0, 24, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks063 = [
    PreviewTrack( 0, 0, 0, 0, 24, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks064 = [
    PreviewTrack( 0, 0, 0, 0, 24, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks065 = [
    PreviewTrack( 0, 0, 0, 0, 24, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks066 = [
    PreviewTrack( 0, 0, 0, 0, 64, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, -32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 4, 0, -32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 5, 0, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 6, 32, -32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 7, 32, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 8, 32, 0, 0, 0, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_1 ),
    TRACK_BLOCK_END
]

TrackBlocks067 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 32, 0, 0, 0, QuarterTile( 0b0000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 | RCT_PREVIEW_TRACK_FLAG_1 ),
    TRACK_BLOCK_END
]

TrackBlocks068 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks069 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks070 = [
    PreviewTrack( 0, 0, 0, 0, 64, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks071 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks072 = [
    PreviewTrack( 0, 0, 0, 0, 32, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks073 = [
    PreviewTrack( 0, 0, 0, 0, 32, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks074 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks075 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks076 = [
    PreviewTrack( 0, 0, 0, 0, 64, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks077 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks078 = [
    PreviewTrack( 0, 0, 0, 0, 32, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks079 = [
    PreviewTrack( 0, 0, 0, 0, 32, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks080 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks081 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, -32, 0, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 4, -32, -64, 0, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, -32, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 6, -64, -64, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks082 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b1110, 0 ), 0 ),
    PreviewTrack( 4, -32, 64, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, 32, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 6, -64, 64, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks083 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 2, -32, -32, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 3, -64, -32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks084 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 2, -32, 32, 0, 0, QuarterTile( 0b1110, 0 ), 0 ),
    PreviewTrack( 3, -64, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks085 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 1, 0, -32, 0, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b0010, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks086 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b0001, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks087 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 1, 0, -32, 0, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 4, QuarterTile( 0b0010, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, 0, 4, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 4, -32, -64, 8, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 5, 0, -64, 8, 0, QuarterTile( 0b0100, 0b0000 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 6, -32, -96, 8, 4, QuarterTile( 0b0001, 0 ), 0 ),
    PreviewTrack( 7, 0, -96, 8, 4, QuarterTile( 0b1011, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks088 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0100, 0b0000 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 4, QuarterTile( 0b0001, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 0, 4, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 4, -32, 64, 8, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 5, 0, 64, 8, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 6, -32, 96, 8, 4, QuarterTile( 0b0010, 0 ), 0 ),
    PreviewTrack( 7, 0, 96, 8, 4, QuarterTile( 0b0111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks089 = [
    PreviewTrack( 0, 0, 0, 8, 4, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 1, 0, -32, 8, 4, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 8, 0, QuarterTile( 0b0010, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, 8, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 4, -32, -64, 0, 4, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 5, 0, -64, 0, 4, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 6, -32, -96, 0, 0, QuarterTile( 0b0001, 0 ), 0 ),
    PreviewTrack( 7, 0, -96, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks090 = [
    PreviewTrack( 0, 0, 0, 8, 4, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 8, 4, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 8, 0, QuarterTile( 0b0001, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 8, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 4, -32, 64, 0, 4, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 5, 0, 64, 0, 4, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 6, -32, 96, 0, 0, QuarterTile( 0b0010, 0 ), 0 ),
    PreviewTrack( 7, 0, 96, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks091 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, -32, 0, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 4, -32, -64, 0, 4, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, -32, 0, 4, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 6, -64, -64, 0, 4, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 7, -64, -96, 8, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 8, -32, -96, 8, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 9, -64, -128, 8, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 10, -32, -128, 8, 0, QuarterTile( 0b1110, 0 ), 0 ),
    PreviewTrack( 11, 0, -128, 8, 4, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 12, -32, -160, 8, 4, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 13, 0, -160, 8, 4, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks092 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b1110, 0 ), 0 ),
    PreviewTrack( 4, -32, 64, 0, 4, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, 32, 0, 4, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 6, -64, 64, 0, 4, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 7, -64, 96, 8, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 8, -32, 96, 8, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 9, -64, 128, 8, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 10, -32, 128, 8, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 11, 0, 128, 8, 4, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 12, -32, 160, 8, 4, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 13, 0, 160, 8, 4, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks093 = [
    PreviewTrack( 0, 0, 0, 8, 4, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, -32, 8, 4, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 8, 4, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, 8, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 4, -32, -64, 8, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, -32, 8, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 6, -64, -64, 8, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 7, -64, -96, 0, 4, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 8, -32, -96, 0, 4, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 9, -64, -128, 0, 4, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 10, -32, -128, 0, 0, QuarterTile( 0b1110, 0 ), 0 ),
    PreviewTrack( 11, 0, -128, 0, 0, QuarterTile( 0b0100, 0b0000 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 12, -32, -160, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 13, 0, -160, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks094 = [
    PreviewTrack( 0, 0, 0, 8, 4, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 8, 4, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 8, 4, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 8, 0, QuarterTile( 0b1110, 0 ), 0 ),
    PreviewTrack( 4, -32, 64, 8, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, 32, 8, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 6, -64, 64, 8, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 7, -64, 96, 0, 4, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 8, -32, 96, 0, 4, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 9, -64, 128, 0, 4, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 10, -32, 128, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 11, 0, 128, 0, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 12, -32, 160, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 13, 0, 160, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks095 = [
    PreviewTrack( 0, 0, 0, 0, 64, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks096 = [
    PreviewTrack( 0, 0, 0, 0, 64, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks097 = [
    PreviewTrack( 0, 0, 0, 0, 64, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks098 = [
    PreviewTrack( 0, 0, 0, 0, 64, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks099 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks100 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks101 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks102 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, -32, 0, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 4, -32, -64, 0, 12, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, -32, 0, 12, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 6, -64, -64, 0, 12, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks103 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b1110, 0 ), 0 ),
    PreviewTrack( 4, -32, 64, 0, 12, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, 32, 0, 12, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 6, -64, 64, 0, 12, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks104 = [
    PreviewTrack( 0, 0, 0, 0, 12, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, -32, 0, 12, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 12, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 4, -32, -64, 0, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, -32, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 6, -64, -64, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks105 = [
    PreviewTrack( 0, 0, 0, 0, 12, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 12, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 12, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b1110, 0 ), 0 ),
    PreviewTrack( 4, -32, 64, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, 32, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 6, -64, 64, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks106 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, -32, 0, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 4, -32, -64, 0, 12, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, -32, 0, 12, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 6, -64, -64, 0, 12, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks107 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b1110, 0 ), 0 ),
    PreviewTrack( 4, -32, 64, 0, 12, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, 32, 0, 12, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 6, -64, 64, 0, 12, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks108 = [
    PreviewTrack( 0, 0, 0, 0, 12, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, -32, 0, 12, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 12, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 4, -32, -64, 0, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, -32, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 6, -64, -64, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks109 = [
    PreviewTrack( 0, 0, 0, 0, 12, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 12, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 12, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b1110, 0 ), 0 ),
    PreviewTrack( 4, -32, 64, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, 32, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 6, -64, 64, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks110 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks111 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks112 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks113 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks114 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks115 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks116 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks117 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),## orig clearance 16
    PreviewTrack( 2, -64, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),## orig clearance 16
    PreviewTrack( 3, -96, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),## orig clearance 16
    PreviewTrack( 4, -128, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks118 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, 16, 24, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, -96, 0, 40, 48, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks119 = [
    PreviewTrack( 0, 0, 0, 0, 48, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 40, 48, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, 64, 24, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, -96, 0, 80, 8, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks120 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks121 = [
    PreviewTrack( 0, 0, 0, 40, 48, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 16, 24, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, -96, 0, 0, 8, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks122 = [
    PreviewTrack( 0, 0, 0, 80, 8, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 64, 24, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, 40, 48, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, -96, 0, 0, 48, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks123 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0b1100 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 8, QuarterTile( 0b1111, 0b0011 ), 0 ),
    PreviewTrack( 2, -64, 0, -32, 32, QuarterTile( 0b1111, 0b0011 ), 0 ),
    PreviewTrack( 3, -96, 0, -96, 64, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks124 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 32, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, 0, 48, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, -96, 0, 0, 80, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 4, -128, 0, 0, 160, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 5, -192, 0, 0, 208, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 6, -160, 0, 0, 208, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks125 = [
    PreviewTrack( 0, 0, 0, 0, 48, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 32, 0, 0, 48, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks126 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 1, 32, 0, 0, 0, QuarterTile( 0b0000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 | RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    TRACK_BLOCK_END
]

TrackBlocks127 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 1, 32, 0, 0, 0, QuarterTile( 0b0000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 | RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    TRACK_BLOCK_END
]

TrackBlocks128 = [
    PreviewTrack( 0, 0, 0, 0, 32, QuarterTile( 0b1111, 0b1100 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 1, 32, 0, 0, 0, QuarterTile( 0b0000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 | RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    TRACK_BLOCK_END
]

TrackBlocks129 = [
    PreviewTrack( 0, 0, 0, 0, 32, QuarterTile( 0b1111, 0b0011 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    TRACK_BLOCK_END
]

TrackBlocks130 = [
    PreviewTrack( 0, 0, 0, 0, 56, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    TRACK_BLOCK_END
]

TrackBlocks131 = [
    PreviewTrack( 0, 0, 0, 0, 56, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 1, 32, 0, 0, 0, QuarterTile( 0b0000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 | RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    TRACK_BLOCK_END
]

TrackBlocks132 = [
    PreviewTrack( 0, 0, 0, 0, 24, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks133 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -32, -32, 0, 0, QuarterTile( 0b1000, 0 ), 0 ),
    PreviewTrack( 3, -64, 0, 0, 0, QuarterTile( 0b0010, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 4, -64, -32, 0, 0, QuarterTile( 0b0001, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks134 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -32, 32, 0, 0, QuarterTile( 0b0100, 0 ), 0 ),
    PreviewTrack( 3, -64, 0, 0, 0, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 4, -64, 32, 0, 0, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks135 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 0, QuarterTile( 0b0001, 0 ), 0 ),
    PreviewTrack( 2, 0, 32, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 4, -64, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks136 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0100, 0 ), 0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 4, -32, 64, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks137 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -32, -32, 0, 0, QuarterTile( 0b1000, 0 ), 0 ),
    PreviewTrack( 3, -64, 0, 0, 0, QuarterTile( 0b0010, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 4, -64, -32, 0, 0, QuarterTile( 0b0001, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks138 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -32, 32, 0, 0, QuarterTile( 0b0100, 0 ), 0 ),
    PreviewTrack( 3, -64, 0, 0, 0, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 4, -64, 32, 0, 0, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks139 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 0, QuarterTile( 0b0001, 0 ), 0 ),
    PreviewTrack( 2, 0, 32, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 4, -64, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks140 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0100, 0 ), 0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 4, -32, 64, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks141 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks142 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 16, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 16, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 16, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks143 = [
    PreviewTrack( 0, 0, 0, 0, 64, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 64, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 64, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 64, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks144 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 8, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 8, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 8, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks145 = [
    PreviewTrack( 0, 0, 0, 0, 32, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 32, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 32, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 32, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks146 = [
    PreviewTrack( 0, 0, 0, 0, 32, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 32, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 32, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 32, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks147 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 8, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 8, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 8, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks148 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 16, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 16, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 16, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks149 = [
    PreviewTrack( 0, 0, 0, 0, 64, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 64, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 64, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 64, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks150 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 8, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 8, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 8, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks151 = [
    PreviewTrack( 0, 0, 0, 0, 32, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 32, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 32, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 32, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks152 = [
    PreviewTrack( 0, 0, 0, 0, 32, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 32, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 32, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 32, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks153 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 8, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 8, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 8, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks154 = [
    PreviewTrack( 0, 0, 0, 0, 24, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 24, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 24, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 24, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks155 = [
    PreviewTrack( 0, 0, 0, 0, 24, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 24, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 24, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 24, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks156 = [
    PreviewTrack( 0, 0, 0, 0, 24, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 24, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 24, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 24, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks157 = [
    PreviewTrack( 0, 0, 0, 0, 24, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 24, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 24, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 24, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks158 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks159 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks160 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks161 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks162 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 8, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 8, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 8, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks163 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 8, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 8, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 8, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks164 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 8, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 8, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 8, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks165 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 8, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 8, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 8, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks166 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 8, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 8, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 8, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks167 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 8, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 8, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 8, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks168 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 8, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 8, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 8, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks169 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 8, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 8, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 8, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks170 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks171 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b0001, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b0010, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks172 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks173 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks174 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks175 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks176 = [
    PreviewTrack( 0, 0, 0, -32, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, -32, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, -32, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks177 = [
    PreviewTrack( 0, 0, 0, -32, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, -32, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, -32, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks178 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b0111, 0b0100 ), 0 ),
    PreviewTrack( 1, 0, -32, 0, 16, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 16, QuarterTile( 0b0010, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, 16, 16,QuarterTile( 0b0111, 0b0110 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks179 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1011, 0b1000 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 16, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 16, QuarterTile( 0b0001, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 16, 16,QuarterTile( 0b1011, 0b1001 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks180 = [
    PreviewTrack( 0, 0, 0, 16, 16,QuarterTile( 0b0111, 0b0011 ), 0 ),
    PreviewTrack( 1, 0, -32, 0, 16, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 16, QuarterTile( 0b0010, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, 0, 0, QuarterTile( 0b0111, 0b0001 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks181 = [
    PreviewTrack( 0, 0, 0, 16, 16, QuarterTile( 0b1011, 0b0011 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 16, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 16, QuarterTile( 0b0001, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b1011, 0b0010 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks182 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks183 = [
    PreviewTrack( 0, 0, 0, 0, 24, QuarterTile( 0b1111, 0b1100 ), 0 ),
    PreviewTrack( 1, -32, 0, 16, 40, QuarterTile( 0b1111, 0b1100 ), 0 ),
    PreviewTrack( 2, -64, 0, 32, 56, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, -96, 0, 64, 192, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 4, -128, -32, 120, 96, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 5, -96, -32, 64, 192, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 6, -64, -32, 248, 16, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks184 = [
    PreviewTrack( 0, 0, 0, 0, 24, QuarterTile( 0b1111, 0b1100 ), 0 ),
    PreviewTrack( 1, -32, 0, 16, 40, QuarterTile( 0b1111, 0b1100 ), 0 ),
    PreviewTrack( 2, -64, 0, 32, 56, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, -96, 0, 64, 192, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 4, -128, 32, 120, 96, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 5, -96, 32, 64, 192, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 6, -64, 32, 248, 16, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks185 = [
    PreviewTrack( 0, 0, 0, -32, 24, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, -216, 192, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, -160, 96, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, -216, 192, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 4, 0, -32, -248, 56, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 5, 32, -32, -264, 40, QuarterTile( 0b1111, 0b1100 ), 0 ),
    PreviewTrack( 6, 64, -32, -280, 24, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks186 = [
    PreviewTrack( 0, 0, 0, -32, 24, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, -216, 192, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, -160, 96, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, -216, 192, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 4, 0, 32, -248, 56, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 5, 32, 32, -264, 40, QuarterTile( 0b1111, 0b1100 ), 0 ),
    PreviewTrack( 6, 64, 32, -280, 24, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks187 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, -16, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, -16, 16, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks188 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, -16, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, -16, 16, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks189 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, 16, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks190 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, 16, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks191 = [
    PreviewTrack( 0, 0, 0, 0, 32, QuarterTile( 0b1111, 0b1100 ), 0 ),
    PreviewTrack( 1, -32, 0, 16, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    PreviewTrack( 2, -64, 0, 32, 96,QuarterTile( 0b0011, 0 ), 0 ),
    PreviewTrack( 3, -32, 0, 120, 16, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks192 = [
    PreviewTrack( 0, 0, 0, 0, 32, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, -88, 96,QuarterTile( 0b0011, 0 ), 0 ),
    PreviewTrack( 2, 0, 0, -104, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    PreviewTrack( 3, 32, 0, -120, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks193 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 24, 32, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 2, -32, -32, 48, 16, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks194 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 24, 32, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 2, -32, 32, 48, 16, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks195 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, -24, 32, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 2, -32, -32, -48, 16, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks196 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, -24, 32, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 2, -32, 32, -48, 16, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks197 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 32, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, 16, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, 0, 0, 32, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks198 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, -32, 32, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, -16, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, 0, 0, -32, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks199 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, -96, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 4, -128, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 5, -160, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks200 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, -96, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 4, -128, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 5, -160, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks201 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks202 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks203 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks204 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -32, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks205 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -32, -32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks206 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 1, -32, 0, -40, 32, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 2, -64, 0, -96, 56, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 3, -96, 0, -96, 0, QuarterTile( 0b0000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 | RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    TRACK_BLOCK_END
]

TrackBlocks207 = [
    PreviewTrack( 0, 0, 0, 0, 56, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 1, 32, 0, 56, 32, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 2, 64, 0, 96, 16, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    TRACK_BLOCK_END
]

TrackBlocks208 = [
    PreviewTrack( 0, 0, 0, -32, 16, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 1, -32, 0, -72, 32, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 2, -64, 0, -128, 56, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 3, -96, 0, -128, 0, QuarterTile( 0b0000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 | RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    TRACK_BLOCK_END
]

TrackBlocks209 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b0111, 0 ), 0 ),
    PreviewTrack( 1, 0, -32, 0, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 8, QuarterTile( 0b0010, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, 0, 8, QuarterTile( 0b0111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks210 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1011, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 0, 8, QuarterTile( 0b0001, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 0, 8, QuarterTile( 0b1011, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks211 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, -32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -32, -32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, -64, -32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 4, -32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 5, -64, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks212 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -32, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, -64, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 4, -32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 5, -64, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks213 = [
    PreviewTrack( 0, 0, 0, 0, 32, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 32, 0, 0, 32, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -64, 0, 0, 32, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, -32, 0, 0, 32, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks214 = [
    PreviewTrack( 0, 0, 0, 0, 48, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 32, 0, 0, 48, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks215 = [
    PreviewTrack( 0, 0, 0, 0, 208, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 32, 0, 0, 208, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -32, 0, 0, 160, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, -64, 0, 0, 80, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 4, -96, 0, 0, 48, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 5, -128, 0, 0, 32, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 6, -160, 0, 0, 16, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks216 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks217 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b0111, 0b0100 ), 0 ),
    PreviewTrack( 1, 0, -32, 16, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 16, 0, QuarterTile( 0b0010, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, 16, 16,QuarterTile( 0b0111, 0b0110 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks218 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1011, 0b1000 ), 0 ),
    PreviewTrack( 1, 0, 32, 16, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 16, 0, QuarterTile( 0b0001, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 16, 16,QuarterTile( 0b1011, 0b1001 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks219 = [
    PreviewTrack( 0, 0, 0, 16, 16,QuarterTile( 0b0111, 0b0011 ), 0 ),
    PreviewTrack( 1, 0, -32, 16, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 16, 0, QuarterTile( 0b0010, 0 ), 0 ),
    PreviewTrack( 3, -32, -32, 0, 16, QuarterTile( 0b0111, 0b0001 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks220 = [
    PreviewTrack( 0, 0, 0, 16, 16, QuarterTile( 0b1011, 0b0011 ), 0 ),
    PreviewTrack( 1, 0, 32, 16, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 16, 0, QuarterTile( 0b0001, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 0, 16, QuarterTile( 0b1011, 0b0010 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks221 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    PreviewTrack( 1, 0, -32, 16, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 16, 16, QuarterTile( 0b0111, 0b0100 ), 0 ),
    PreviewTrack( 3, -32, -32, 24, 16, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 4, -32, -64, 48, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, -32, 32, 16, QuarterTile( 0b0111, 0b0100 ), 0 ),
    PreviewTrack( 6, -64, -64, 48, 16, QuarterTile( 0b1111, 0b0110 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks222 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    PreviewTrack( 1, 0, 32, 16, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 16, 16, QuarterTile( 0b1011, 0b1000 ), 0 ),
    PreviewTrack( 3, -32, 32, 24, 16, QuarterTile( 0b1110, 0 ), 0 ),
    PreviewTrack( 4, -32, 64, 48, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, 32, 32, 16, QuarterTile( 0b1011, 0b1000 ), 0 ),
    PreviewTrack( 6, -64, 64, 48, 16, QuarterTile( 0b1111, 0b1001 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks223 = [
    PreviewTrack( 0, 0, 0, 48, 16, QuarterTile( 0b1111, 0b0011 ), 0 ),
    PreviewTrack( 1, 0, -32, 48, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 32, 16, QuarterTile( 0b0111, 0b0001 ), 0 ),
    PreviewTrack( 3, -32, -32, 24, 16, QuarterTile( 0b1101, 0 ), 0 ),
    PreviewTrack( 4, -32, -64, 16, 0, QuarterTile( 0b1000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, -32, 16, 16, QuarterTile( 0b0111, 0b0001 ), 0 ),
    PreviewTrack( 6, -64, -64, 0, 16, QuarterTile( 0b1111, 0b1001 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks224 = [
    PreviewTrack( 0, 0, 0, 48, 16, QuarterTile( 0b1111, 0b0011 ), 0 ),
    PreviewTrack( 1, 0, 32, 48, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 2, -32, 0, 32, 16, QuarterTile( 0b1011, 0b0010 ), 0 ),
    PreviewTrack( 3, -32, 32, 24, 16, QuarterTile( 0b1110, 0 ), 0 ),
    PreviewTrack( 4, -32, 64, 16, 0, QuarterTile( 0b0100, 0 ), RCT_PREVIEW_TRACK_FLAG_0 ),
    PreviewTrack( 5, -64, 32, 16, 16, QuarterTile( 0b1011, 0b0010 ), 0 ),
    PreviewTrack( 6, -64, 64, 0, 16, QuarterTile( 0b1111, 0b0110 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks225 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks226 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks227 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks228 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks229 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks230 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks231 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks232 = [
    PreviewTrack( 0, 0, 0, 0, 16, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks233 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks234 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks235 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks236 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks237 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks238 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks239 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks240 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks241 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks242 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks243 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks244 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks245 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks246 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0b0011 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks247 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks248 = [
    PreviewTrack( 0, 0, 0, 0, 8, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocks249 = [
    PreviewTrack( 0, 0, 0, 0, 72, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 | RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    TRACK_BLOCK_END
]

TrackBlocks250 = [
    PreviewTrack( 0, 0, 0, 0, 72, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 1, 0, -32, 0, 0, QuarterTile( 0b0000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 | RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    TRACK_BLOCK_END
]

TrackBlocks251 = [
    PreviewTrack( 0, 0, 0, 0, 72, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b0000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 | RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    TRACK_BLOCK_END
]

TrackBlocks252 = [
    PreviewTrack( 0, 0, 0, 0, 72, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 1, 0, -32, 0, 0, QuarterTile( 0b0000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 | RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    TRACK_BLOCK_END
]

TrackBlocks253 = [
    PreviewTrack( 0, 0, 0, 0, 56, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 1, 32, 0, 56, 32, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 2, 64, 0, 96, 16, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    TRACK_BLOCK_END
]

TrackBlocks254 = [
    PreviewTrack( 0, 0, 0, -32, 16, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 1, -32, 0, -72, 32, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 2, -64, 0, -128, 56, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 3, -96, 0, -128, 0, QuarterTile( 0b0000, 0 ), RCT_PREVIEW_TRACK_FLAG_0 | RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    TRACK_BLOCK_END
]

TrackBlocks255 = [
    PreviewTrack( 0, 0, 0, 32, 56, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 1, 32, 0, 88, 32, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    PreviewTrack( 2, 64, 0, 128, 16, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_IS_VERTICAL ),
    TRACK_BLOCK_END
]

TrackBlocksRotationControlToggle = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0b1100 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocksFlatTrack1x4A = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -64, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, 32, 0, 0, 0, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_1 ),
    TRACK_BLOCK_END
]

TrackBlocksFlatTrack2x2 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, 32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, 32, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocksFlatTrack4x4 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, 0, 64, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, 0, 96, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 4, 32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 5, 32, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 6, 32, 64, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 7, 32, 96, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 8, 64, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 9, 64, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 10, 64, 64, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 11, 64, 96, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 12, 96, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 13, 96, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 14, 96, 64, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 15, 96, 96, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocksFlatTrack2x4 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, 0, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, 0, 64, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, 0, 96, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 4, 32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 5, 32, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 6, 32, 64, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 7, 32, 96, 0, 0, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_1 ),
    TRACK_BLOCK_END
]

TrackBlocksFlatTrack1x5 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -64, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, 32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 4, 64, 0, 0, 0, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_1 ),
    TRACK_BLOCK_END
]

TrackBlocksFlatTrack1x1A = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocksFlatTrack1x4B = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -64, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, 32, 0, 0, 0, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_1 ),
    TRACK_BLOCK_END
]

TrackBlocksFlatTrack1x1B = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    TRACK_BLOCK_END
]

TrackBlocksFlatTrack1x4C = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -64, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, 32, 0, 0, 0, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_1 ),
    TRACK_BLOCK_END
]

TrackBlocksFlatTrack3x3 = [
    PreviewTrack( 0, 0, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 1, -32, -32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 2, -32, 0, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 3, -32, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 4, 0, -32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 5, 0, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 6, 32, -32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 7, 32, 32, 0, 0, QuarterTile( 0b1111, 0 ), 0 ),
    PreviewTrack( 8, 32, 0, 0, 0, QuarterTile( 0b1111, 0 ), RCT_PREVIEW_TRACK_FLAG_1 ),
    TRACK_BLOCK_END
]

TRACK_BLOCKS = [
    TrackBlocks000,
    TrackBlocks001,
    TrackBlocks002,
    TrackBlocks003,
    TrackBlocks004,
    TrackBlocks005,
    TrackBlocks006,
    TrackBlocks007,
    TrackBlocks008,
    TrackBlocks009,
    TrackBlocks010,
    TrackBlocks011,
    TrackBlocks012,
    TrackBlocks013,
    TrackBlocks014,
    TrackBlocks015,
    TrackBlocks016,
    TrackBlocks017,
    TrackBlocks018,
    TrackBlocks019,
    TrackBlocks020,
    TrackBlocks021,
    TrackBlocks022,
    TrackBlocks023,
    TrackBlocks024,
    TrackBlocks025,
    TrackBlocks026,
    TrackBlocks027,
    TrackBlocks028,
    TrackBlocks029,
    TrackBlocks030,
    TrackBlocks031,
    TrackBlocks032,
    TrackBlocks033,
    TrackBlocks034,
    TrackBlocks035,
    TrackBlocks036,
    TrackBlocks037,
    TrackBlocks038,
    TrackBlocks039,
    TrackBlocks040,
    TrackBlocks041,
    TrackBlocks042,
    TrackBlocks043,
    TrackBlocks044,
    TrackBlocks045,
    TrackBlocks046,
    TrackBlocks047,
    TrackBlocks048,
    TrackBlocks049,
    TrackBlocks050,
    TrackBlocks051,
    TrackBlocks052,
    TrackBlocks053,
    TrackBlocks054,
    TrackBlocks055,
    TrackBlocks056,
    TrackBlocks057,
    TrackBlocks058,
    TrackBlocks059,
    TrackBlocks060,
    TrackBlocks061,
    TrackBlocks062,
    TrackBlocks063,
    TrackBlocks064,
    TrackBlocks065,
    TrackBlocks066,
    TrackBlocks067,
    TrackBlocks068,
    TrackBlocks069,
    TrackBlocks070,
    TrackBlocks071,
    TrackBlocks072,
    TrackBlocks073,
    TrackBlocks074,
    TrackBlocks075,
    TrackBlocks076,
    TrackBlocks077,
    TrackBlocks078,
    TrackBlocks079,
    TrackBlocks080,
    TrackBlocks081,
    TrackBlocks082,
    TrackBlocks083,
    TrackBlocks084,
    TrackBlocks085,
    TrackBlocks086,
    TrackBlocks087,
    TrackBlocks088,
    TrackBlocks089,
    TrackBlocks090,
    TrackBlocks091,
    TrackBlocks092,
    TrackBlocks093,
    TrackBlocks094,
    TrackBlocks095,
    TrackBlocks096,
    TrackBlocks097,
    TrackBlocks098,
    TrackBlocks099,
    TrackBlocks100,
    TrackBlocks101,
    TrackBlocks102,
    TrackBlocks103,
    TrackBlocks104,
    TrackBlocks105,
    TrackBlocks106,
    TrackBlocks107,
    TrackBlocks108,
    TrackBlocks109,
    TrackBlocks110,
    TrackBlocks111,
    TrackBlocks112,
    TrackBlocks113,
    TrackBlocks114,
    TrackBlocks115,
    TrackBlocks116,
    TrackBlocks117,
    TrackBlocks118,
    TrackBlocks119,
    TrackBlocks120,
    TrackBlocks121,
    TrackBlocks122,
    TrackBlocks123,
    TrackBlocks124,
    TrackBlocks125,
    TrackBlocks126,
    TrackBlocks127,
    TrackBlocks128,
    TrackBlocks129,
    TrackBlocks130,
    TrackBlocks131,
    TrackBlocks132,
    TrackBlocks133,
    TrackBlocks134,
    TrackBlocks135,
    TrackBlocks136,
    TrackBlocks137,
    TrackBlocks138,
    TrackBlocks139,
    TrackBlocks140,
    TrackBlocks141,
    TrackBlocks142,
    TrackBlocks143,
    TrackBlocks144,
    TrackBlocks145,
    TrackBlocks146,
    TrackBlocks147,
    TrackBlocks148,
    TrackBlocks149,
    TrackBlocks150,
    TrackBlocks151,
    TrackBlocks152,
    TrackBlocks153,
    TrackBlocks154,
    TrackBlocks155,
    TrackBlocks156,
    TrackBlocks157,
    TrackBlocks158,
    TrackBlocks159,
    TrackBlocks160,
    TrackBlocks161,
    TrackBlocks162,
    TrackBlocks163,
    TrackBlocks164,
    TrackBlocks165,
    TrackBlocks166,
    TrackBlocks167,
    TrackBlocks168,
    TrackBlocks169,
    TrackBlocks170,
    TrackBlocks171,
    TrackBlocks172,
    TrackBlocks173,
    TrackBlocks174,
    TrackBlocks175,
    TrackBlocks176,
    TrackBlocks177,
    TrackBlocks178,
    TrackBlocks179,
    TrackBlocks180,
    TrackBlocks181,
    TrackBlocks182,
    TrackBlocks183,
    TrackBlocks184,
    TrackBlocks185,
    TrackBlocks186,
    TrackBlocks187,
    TrackBlocks188,
    TrackBlocks189,
    TrackBlocks190,
    TrackBlocks191,
    TrackBlocks192,
    TrackBlocks193,
    TrackBlocks194,
    TrackBlocks195,
    TrackBlocks196,
    TrackBlocks197,
    TrackBlocks198,
    TrackBlocks199,
    TrackBlocks200,
    TrackBlocks201,
    TrackBlocks202,
    TrackBlocks203,
    TrackBlocks204,
    TrackBlocks205,
    TrackBlocks206,
    TrackBlocks207,
    TrackBlocks208,
    TrackBlocks209,
    TrackBlocks210,
    TrackBlocks211,
    TrackBlocks212,
    TrackBlocks213,
    TrackBlocks214,
    TrackBlocks215,
    TrackBlocks216,
    TrackBlocks217,
    TrackBlocks218,
    TrackBlocks219,
    TrackBlocks220,
    TrackBlocks221,
    TrackBlocks222,
    TrackBlocks223,
    TrackBlocks224,
    TrackBlocks225,
    TrackBlocks226,
    TrackBlocks227,
    TrackBlocks228,
    TrackBlocks229,
    TrackBlocks230,
    TrackBlocks231,
    TrackBlocks232,
    TrackBlocks233,
    TrackBlocks234,
    TrackBlocks235,
    TrackBlocks236,
    TrackBlocks237,
    TrackBlocks238,
    TrackBlocks239,
    TrackBlocks240,
    TrackBlocks241,
    TrackBlocks242,
    TrackBlocks243,
    TrackBlocks244,
    TrackBlocks245,
    TrackBlocks246,
    TrackBlocks247,
    TrackBlocks248,
    TrackBlocks249,
    TrackBlocks250,
    TrackBlocks251,
    TrackBlocks252,
    TrackBlocks253,
    TrackBlocks254,
    TrackBlocks255,
    TrackBlocksRotationControlToggle,

    TrackBlocksFlatTrack1x4A,
    TrackBlocksFlatTrack2x2,
    TrackBlocksFlatTrack4x4,
    TrackBlocksFlatTrack2x4,
    TrackBlocksFlatTrack1x5,
    TrackBlocksFlatTrack1x1A,
    TrackBlocksFlatTrack1x4B,
    TrackBlocksFlatTrack1x1B,
    TrackBlocksFlatTrack1x4C,
    TrackBlocksFlatTrack3x3,
]