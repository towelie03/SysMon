import { useContext, useEffect, useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { ProcessListView } from "./views/process/ProcessListView";
import { SettingsView } from "./views/settings/SettingsView";
import { RealtimeDataProvider } from "./views/system/realtime/realtime_data_provider";
import { SystemMonitorView } from "./views/system/SystemMonitorView";
import { ThemeContext } from "./theme_provider";
import { cn } from "./lib/utils";
import { Toaster } from "./components/ui/sonner";
import useWebSocket, { ReadyState } from 'react-use-websocket';
import { toast } from "sonner";

function App() {
  let theme = useContext(ThemeContext);

  const [socketUrl, setSocketUrl] = useState('ws://localhost:8000/notification');
  const [messageHistory, setMessageHistory] = useState<MessageEvent<any>[]>([]);

  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);

  useEffect(() => {
    if (lastMessage !== null) {
      console.log(lastMessage)
      let parsed_data = JSON.parse(lastMessage.data)

      toast.message(parsed_data["title"], {description: parsed_data["msg"]})
      setMessageHistory((prev) => prev.concat(lastMessage));
    }
  }, [lastMessage]);

  return (
    <div className={cn("bg-background w-screen h-screen p-4", theme.theme)}>
      <RealtimeDataProvider>
        <Tabs
          defaultValue="system"
          className="flex flex-col items-center w-full h-full text-foreground"
        >
          <TabsList className="flex justify-center items-center w-fit">
            <TabsTrigger value="processes">Processes</TabsTrigger>
            <TabsTrigger value="system">System</TabsTrigger>
            <TabsTrigger value="settings">Settings</TabsTrigger>
          </TabsList>
          <TabsContent
            value="processes"
            className="w-full h-full p-4 rounded-md bg-card ring-2 ring-accent mt-4 overflow-x-hidden"
          >
            <ProcessListView></ProcessListView>
          </TabsContent>

          <TabsContent
            value="system"
            className="w-full h-full p-4 rounded-md bg-card ring-2 ring-accent mt-4"
          >
            <SystemMonitorView></SystemMonitorView>
          </TabsContent>

          <TabsContent
            value="settings"
            className="w-full h-full p-4 rounded-md bg-card ring-2 ring-accent mt-4"
          >
            <SettingsView></SettingsView>
          </TabsContent>
        </Tabs>
      </RealtimeDataProvider>
      <Toaster expand/>
    </div>
  );
}

export default App;
