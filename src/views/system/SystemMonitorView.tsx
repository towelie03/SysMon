import { useContext, useState } from "react";
import { Separator } from "../../components/ui/separator";
import { Line, LineChart, ResponsiveContainer, YAxis } from "recharts";
import { CpuInfoView } from "./cpu/cpu_info_view";
import { MemoryInfoView } from "./memory/memory_info_view";
import { RealtimeDataContext } from "./realtime/realtime_data_context";
import { DiskInfoView } from "./disk/disk_info_view";

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
  const realtimeData = useContext(RealtimeDataContext);

  const [page, setPage] = useState(0);

  function getCpuPerc() {
    var obj: any = realtimeData[realtimeData.length - 1];
    if (obj === undefined) return "0";
    return obj.cpu_usage;
  }

  function getMemoryPerc() {
    var obj: any = realtimeData[realtimeData.length - 1];
    if (obj === undefined) return "Unknown";
    return `${(obj.memory_usage / 1024 / 1024 / 1024).toFixed(2)} / ${(
      obj.memory_total /
      1024 /
      1024 /
      1024
    ).toFixed(2)} GB (${obj.memory_percent}%)`;
  }

  function getDiskActiveTime() {
    var obj: any = realtimeData[realtimeData.length - 1];
    if (obj === undefined) return "0";
    return obj.disk_active_time;
  }

  function renderPage() {
    switch (page) {
      case 0:
        return <CpuInfoView></CpuInfoView>;
      case 1:
        return <MemoryInfoView></MemoryInfoView>;
      case 2:
        return <DiskInfoView></DiskInfoView>
      default:
        return <CpuInfoView></CpuInfoView>;
    }
  }

  return (
    <div className="flex flex-row w-full h-full">
      <div className="bg-popover flex flex-col w-[30%] h-full gap-4 pr-4">
        <div
          className="flex flex-row h-full w-full accent-chart-1 hover:bg-black/10 transition-colors cursor-pointer rounded-md"
          onClick={() => {
            setPage(0);
          }}
        >
          <ResponsiveContainer height="100%" width="50%">
            <LineChart
              width={200}
              height={100}
              data={realtimeData}
              className="bg-muted h-full rounded-lg"
            >
              <YAxis domain={[0, 100]} hide />
              <Line
                type="monotone"
                dataKey="cpu_usage"
                stroke={`hsl(var(--primary))`}
                dot={false}
                strokeWidth={2}
                min={0}
                max={100}
              />
            </LineChart>
          </ResponsiveContainer>
          <div className="w-[50%] pl-4 pt-2">
            <div className="font-semibold text-3xl">CPU</div>
            <div className="mt-0 text-lg text-muted-foreground">
              {getCpuPerc()}% 3.82Ghz
            </div>
          </div>
        </div>
        <Separator></Separator>

        <div
          className="flex flex-row h-full w-full accent-chart-1 hover:bg-black/10 transition-colors cursor-pointer rounded-md"
          onClick={() => {
            setPage(1);
          }}
        >
          <ResponsiveContainer height="100%" width="50%">
            <LineChart
              width={200}
              height={100}
              data={realtimeData}
              className="bg-muted h-full rounded-lg"
            >
              <YAxis domain={[0, 100]} hide />
              <Line
                type="monotone"
                dataKey="memory_percent"
                stroke="hsl(var(--primary))"
                dot={false}
                strokeWidth={2}
                min={0}
                max={100}
              />
            </LineChart>
          </ResponsiveContainer>
          <div className="w-[50%] pl-4 pt-2">
            <div className="font-semibold text-3xl">Memory</div>
            <div className="mt-0 text-lg text-muted-foreground">
              {getMemoryPerc()}
            </div>
          </div>
        </div>
        <Separator></Separator>

        <div
          className="flex flex-row h-full w-full accent-chart-1 hover:bg-black/10 transition-colors cursor-pointer rounded-md"
          onClick={() => {
            setPage(2);
          }}
        >
          <ResponsiveContainer height="100%" width="50%">
            <LineChart
              width={200}
              height={100}
              data={realtimeData}
              className="bg-muted h-full rounded-lg"
            >
              <YAxis domain={[0, 100]} hide />
              <Line
                type="monotone"
                dataKey="disk_active_time"
                stroke="hsl(var(--primary))"
                dot={false}
                strokeWidth={2}
                min={0}
                max={100}
              />
            </LineChart>
          </ResponsiveContainer>
          <div className="w-[50%] pl-4 pt-2">
            <div className="font-semibold text-3xl">Disk 0</div>
            <div className="mt-0 text-lg text-muted-foreground">SSD ({getDiskActiveTime()}%)</div>
          </div>
        </div>
        <Separator></Separator>

        <div
          className="flex flex-row h-full w-full accent-chart-1 hover:bg-black/10 transition-colors cursor-pointer rounded-md"
          onClick={() => {
            setPage(3);
          }}
        >
          <ResponsiveContainer height="100%" width="50%">
            <LineChart
              width={200}
              data={data}
              className="bg-muted h-full rounded-lg"
            >
              <Line
                type="monotone"
                dataKey="pv"
                stroke="hsl(var(--primary))"
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
          <div className="w-[50%] pl-4 pt-2">
            <div className="font-semibold text-3xl">Network</div>
            <div className="mt-0 text-lg text-muted-foreground">20 Kbps</div>
          </div>
        </div>
        <Separator></Separator>
      </div>
      <div className="w-full bg-muted rounded-md p-4">{renderPage()}</div>
    </div>
  );
}
