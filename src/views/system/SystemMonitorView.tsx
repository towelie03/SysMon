import { useContext } from "react";
import { Separator } from "../../components/ui/separator";
import { Line, LineChart, ResponsiveContainer, YAxis } from "recharts";
import { CpuDataContext } from "./cpu/cpu_data_context";

const data = [
  {
    name: "Page A",
    uv: 4000,
    pv: 2400,
    amt: 2400,
  },
  {
    name: "Page B",
    uv: 3000,
    pv: 1398,
    amt: 2210,
  },
  {
    name: "Page C",
    uv: 2000,
    pv: 9800,
    amt: 2290,
  },
  {
    name: "Page D",
    uv: 2780,
    pv: 3908,
    amt: 2000,
  },
  {
    name: "Page E",
    uv: 1890,
    pv: 4800,
    amt: 2181,
  },
  {
    name: "Page F",
    uv: 2390,
    pv: 3800,
    amt: 2500,
  },
  {
    name: "Page G",
    uv: 3490,
    pv: 4300,
    amt: 2100,
  },
];

export function SystemMonitorView() {
  const cpuPerc = useContext(CpuDataContext);

  function getCpuPerc() {
    var obj: any = cpuPerc[cpuPerc.length - 1]
    if (obj === undefined) 
        return "0"
    return obj.amt
  }

  return (
    <div className="flex flex-row w-full h-full">
      <div className="bg-popover flex flex-col w-[30%] h-full gap-4 pr-4">
        <div className="flex flex-row h-full w-full accent-chart-1">
          <ResponsiveContainer height="100%" width="50%">
            <LineChart
              width={200}
              height={100}
              data={cpuPerc}
              className="bg-muted h-full rounded-lg"
            >
              <YAxis domain={[0, 100]} hide />
              <Line
                type="monotone"
                dataKey="amt"
                stroke="#8884d8"
                dot={false}
                strokeWidth={2}
                min={0}
                max={100}
              />
            </LineChart>
          </ResponsiveContainer>
          <div className="w-[50%] pl-4 ">
            <div className="font-semibold text-3xl">CPU</div>
            <div className="mt-0 text-lg text-muted-foreground">
              {getCpuPerc()}% 3.82Ghz
            </div>
          </div>
        </div>
        <Separator></Separator>

        <div className="flex flex-row h-full w-full">
          <ResponsiveContainer height="100%" width="50%">
            <LineChart
              width={200}
              height={100}
              data={data}
              className="bg-muted h-full rounded-lg"
            >
              <Line
                type="monotone"
                dataKey="pv"
                stroke="#8884d8"
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
          <div className="w-[50%] pl-4 ">
            <div className="font-semibold text-3xl">Memory</div>
            <div className="mt-0 text-lg text-muted-foreground">
              9.81 / 31.8 GB (31%)
            </div>
          </div>
        </div>
        <Separator></Separator>

        <div className="flex flex-row h-full w-full">
          <ResponsiveContainer height="100%" width="50%">
            <LineChart
              width={200}
              height={100}
              data={data}
              className="bg-muted h-full rounded-lg"
            >
              <Line
                type="monotone"
                dataKey="pv"
                stroke="#8884d8"
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
          <div className="w-[50%] pl-4 ">
            <div className="font-semibold text-3xl">Disk 0</div>
            <div className="mt-0 text-lg text-muted-foreground">SSD (5%)</div>
          </div>
        </div>
        <Separator></Separator>

        <div className="flex flex-row h-full w-full">
          <ResponsiveContainer height="100%" width="50%">
            <LineChart
              width={200}
              data={data}
              className="bg-muted h-full rounded-lg"
            >
              <Line
                type="monotone"
                dataKey="pv"
                stroke="#8884d8"
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
          <div className="w-[50%] pl-4 ">
            <div className="font-semibold text-3xl">Network</div>
            <div className="mt-0 text-lg text-muted-foreground">20 Kbps</div>
          </div>
        </div>
        <Separator></Separator>
      </div>
      <div className="w-full bg-muted rounded-md p-4">abcd</div>
    </div>
  );
}
