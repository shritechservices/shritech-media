// All dates shown in India time (IST, UTC+5:30), same as the web portal.
const OFF = 330 * 60000;
export const ist = (d: string | number | Date) => new Date(new Date(d).getTime() + OFF); // read with getUTC*
export const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
export const MON = MONTHS.map((m) => m.slice(0, 3));
export const DOW = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
export const dayKey = (d: string | number | Date) => { const x = ist(d); return `${x.getUTCFullYear()}-${String(x.getUTCMonth() + 1).padStart(2, '0')}-${String(x.getUTCDate()).padStart(2, '0')}`; };
export const timeStr = (d: string | number | Date) => { const x = ist(d); let h = x.getUTCHours(); const m = x.getUTCMinutes(); const ap = h >= 12 ? 'PM' : 'AM'; h = h % 12 || 12; return `${h}:${String(m).padStart(2, '0')} ${ap}`; };
export const dateStr = (d: string | number | Date, withYear = false) => { const x = ist(d); return `${DOW[x.getUTCDay()]}, ${x.getUTCDate()} ${MON[x.getUTCMonth()]}${withYear ? ' ' + x.getUTCFullYear() : ''}`; };
/** IST wall-clock → ISO (UTC) */
export const fromIST = (y: number, m: number, d: number, hh: number, mm: number) => new Date(Date.UTC(y, m, d, hh, mm) - OFF).toISOString();
export const monthStartISO = (y: number, m: number) => new Date(Date.UTC(y, m, 1) - OFF).toISOString();
export const nowYM = () => { const x = ist(Date.now()); return { y: x.getUTCFullYear(), m: x.getUTCMonth() }; };
export const greet = () => { const h = ist(Date.now()).getUTCHours(); return h < 12 ? 'Good morning' : h < 17 ? 'Good afternoon' : 'Good evening'; };
