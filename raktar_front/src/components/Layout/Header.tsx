import {Box, Burger, Flex, Image, Text} from "@mantine/core";
import UserMenuDropdown from "./UserMenuDropdown.tsx";

const Header = ({opened, toggle}: any) => {
    return (
        <Flex
            justify="space-between"
            style={{display: "flex", alignItems: "center", height: "100%", paddingLeft: '20px', paddingRight: '20px'}}
        >
            <Image src="/logo.png" alt="img" w={80} px={5}/>
            <Text style={{ fontSize: 'clamp(1.5rem, 4vw, 2.5rem)', fontWeight: 700 }}>Raktár</Text>
            <Box>
                <UserMenuDropdown/>
            </Box>
            <Burger
                opened={opened}
                onClick={toggle}
                hiddenFrom="sm"
                size="sm"
                mx={15}
            />
        </Flex>
    );
};

export default Header;
