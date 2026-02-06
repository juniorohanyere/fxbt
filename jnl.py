import sys
import json

from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

class Journal:
    def __init__(self):
        self.json_file = 'jnl.json'
        self.jnl = ""

    #def r_journal(self):

    def from_json(self):
        try:
            with open (self.json_file, 'r') as file:
                rfile = file.read()
        except (FileNotFoundError) as e:
            print(e)
            sys.exit(2)


        ld = json.loads(rfile)

        return ld

    def sort_jnl(self):
        entries = self.from_json()["entries"]

        ents = []
        for entry in entries:
            #d_s = entry["date_set"]
            #d_o = entry["date_opened"]
            #d_c = entry["date_closed"]
            new = entry.copy()
            yy, mm, dd, hh, mn, ss = entry["date_set"]
            new["date_set"] = datetime(yy, mm, dd, hh, mn, ss)

            yy, mm, dd, hh, mn, ss = entry["date_opened"]
            new["date_opened"] = datetime(yy, mm, dd, hh, mn, ss)

            yy, mm, dd, hh, mn, ss = entry["date_closed"]
            new["date_closed"] = datetime(yy, mm, dd, hh, mn, ss)

            ents.append(new)

        srtd = sorted(ents, key=lambda x: x["date_set"])

        return srtd

class BackTest(Journal):
    def __init__(self):
        super().__init__()
        self.jnl = self.sort_jnl()

        self.deci = Decimal("0.01")

        bal = Decimal("0")
        self.bal = bal.quantize(self.deci, rounding=ROUND_HALF_UP)

        risk = Decimal("0.02")
        self.risk = risk.quantize(self.deci, rounding=ROUND_HALF_UP)

        self.a_list = []

    def bktest(self, cap):
        val = Decimal(str(cap))
        self.bal = val.quantize(self.deci, rounding=ROUND_HALF_UP)

        for entry in self.jnl:
            new = {"actv": entry["date_set"]}
            actvs = self.a_list + [new]
            srtd = sorted(actvs, key=lambda x: x["actv"])

            for actv in srtd:
                #print(actv)
                if actv == new:
                    #print("empty")
                    #self.a_list = []
                    rr = entry["rr"]
                    risk = self.risk * self.bal


                    val = Decimal(str(rr))
                    rr = val.quantize(self.deci, rounding=ROUND_HALF_UP)

                    val = Decimal(str(risk))
                    risk = val.quantize(self.deci, rounding=ROUND_HALF_UP)

                    pnl = risk * rr
                    val = Decimal(str(pnl))

                    pnl = val.quantize(self.deci, rounding=ROUND_HALF_UP)
                    print(rr)
                    print(pnl)
                    print("------")

                    self.a_list += [
                        {
                            "pnl": pnl,
                            "actv": entry["date_closed"],
                        }
                    ]

                    break

                else:
                    self.a_list.pop(0)
                    self.bal += actv["pnl"]
                    print(f'\t{self.bal}')
                    #print(self.bal)
                    print("\n")

        self.bal += self.a_list[0]["pnl"]
        print(f'\t{self.bal}')
        print()


if __name__ == '__main__':
    bktest = BackTest()

    bktest.bktest(300)
