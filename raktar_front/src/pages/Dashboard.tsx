import {useEffect} from "react";
import { Card, Title, Text } from '@mantine/core';

const Dashboard = () => {

    useEffect(() => {
        loadItems();
    }, []);

    const loadItems = () => {

    }

    return <div>
    <Card shadow="sm" padding="lg" radius="md" withBorder>
        
        <Title order={2} style={{fontSize: 'clamp(1rem, 4vw, 1.5rem)', lineHeight: 1.2, fontWeight: 700}}>Raktár projekt</Title><br />
        <Text style={{ fontSize: 'clamp(1rem, 2.5vw, 1.5rem)' }}>
          A megrendelő a rendszerben leadhatja az áru megrendelését, megadva a kívánt termékeket és mennyiségeket. A leadott megrendelés szükség esetén módosítható, például a darabszám vagy a termék típusának változása esetén. A rendszer a megrendelés leadása után 24 órával lezárja a megrendelést, utána már nem módosítható. A megrendelések leadása után a megrendelő számára elérhető a megrendelések megtekintése, ahol nyomon követheti az aktuális rendelései állapotát. A rendszer lehetőséget biztosít a megrendelő számára hogy visszajelezzen az árú megérkezéséről és ha bármilyen probléma adódik a megrendeléssel akkor a felhasználó reklamációt indíthat. A rendszer a megrendelők számára biztosítja a személyes adatok, például telefonszám és e-mail cím módosításának lehetőségét, hogy mindig naprakész információkat tartalmazzon a rendszer. <br /><br />
A beszállító szerepe a megrendelt áruk szállítása a raktárba. A rendszerben megnézheti a szállítandó termékeket, az áruszállítási űrlap kitöltésével adhatja meg a szállítással kapcsolatos adatokat, például a várható szállítási időpontot és a szállítandó termékeket. <br /><br />
A fuvarozók a rendszerben nyomon követhetik a fuvarok állapotát, és a megrendeléshez hozzájuk rendelt áruk szállításával kapcsolatos feladatokat végezhetik el. Szükség esetén módosíthatják a fuvar állapotát, például amikor a szállítás elindult vagy befejeződött. <br /> <br />
A raktárosok fő feladata a beérkezett áruk kezelése. Amikor az áru megérkezik a raktárba, a raktáros hozzárendeli azt a megfelelő tárhelyhez. Ezen túlmenően a raktárosok felelősek az áru kiadásának jelzéséért is, amikor az áru elhagyja a raktárt. A raktárosok szintén megtekinthetik a rendszerben a megrendeléseket, és hozzá tudnak rendelni egy fuvarozót a megrendeléshez, biztosítva ezzel a logisztikai folyamatok zökkenőmentes működését. <br />
        </Text>
        
    </Card>
    </div>
   
}

export default Dashboard;