import { useEffect, useState } from "react";
import { Process, columns } from "./table/columns";
import { DataTable } from "./table/data-table";
import { cn } from "@/lib/utils";

export const LoadingSpinner = ({ className }: { className: String }) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={cn("animate-spin", className)}
    >
      <path d="M21 12a9 9 0 1 1-6.219-8.56" />
    </svg>
  );
};

export function ProcessListView() {
  let [isLoading, setIsLoading] = useState(false);
  let [data, setData] = useState([]);

  useEffect(() => {
    let intervalId: NodeJS.Timeout;

    let asyncBridge = async () => {
      let ret = await fetch("http://127.0.0.1:8000/processes");
      let retJson = await ret.json();

      setData(retJson);
      intervalId = setInterval(async () => {
        let ret = await fetch("http://127.0.0.1:8000/processes");
        let retJson = await ret.json();

        setData(retJson);
      }, 2000);
    };

    asyncBridge();

    return () => clearTimeout(intervalId);
  }, []);

  return isLoading ? (
    <LoadingSpinner className=""></LoadingSpinner>
  ) : (
    <div className="h-full">
      <DataTable columns={columns} data={data}></DataTable>
    </div>
  );
}
