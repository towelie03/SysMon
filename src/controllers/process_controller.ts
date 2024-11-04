export async function kill_process(pid: number) {
  await fetch(`http://127.0.0.1:8000/killprocess/${pid}`, {
    method: "POST",
  });
}
