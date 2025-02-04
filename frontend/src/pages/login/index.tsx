import { Link, useNavigate } from "react-router-dom";
import { Container } from "../../components/container";
import { Input } from "../../components/input";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import logoImg from "../../assets/logoEcomerce_transparent.png"
import { useContext } from "react";
import { AuthContext } from "../../contexts/AuthContext";

const schema = z.object({
    email: z.string().email("Insira um email válido").nonempty("O campo email é obrigatório"),
    password: z.string().nonempty("O campo senha é obrigatório")
})

type FormData = z.infer<typeof schema>
// bg-blue-500 hover:bg-blue-600 font-bold py-2 px-4 rounded
export function Login(){
    const { handleLogin, loadingAuth, setLoadingAuth} = useContext(AuthContext);
    const navigate = useNavigate();
    const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
        resolver: zodResolver(schema),
        mode: "onChange"
    })
    
    async function onSubmit(data: FormData) {
        try {
            await handleLogin(data.email, data.password);
            console.log("Usuário logado com sucesso!");
            navigate("/", { replace: true });
        } catch (err) {
            console.error('Erro ao logar usuário:', err);
        }finally {
            setLoadingAuth(false)
        }
    }
    
    return(
        <Container>
            <div className="w-full min-h-screen flex justify-center items-center flex-col gap-4">
            <Link to="/" className="mb-1 max-w-sm w-full">
                <img
                src={logoImg}
                alt="Logo do site"
                className="w-full"
                />
            </Link>
    
            <form
                className="bg-white max-w-xl w-full rounded-lg bg"
                onSubmit={handleSubmit(onSubmit)}
            >
                <div className="mb-3">
                <Input
                    type="email"
                    placeholder="Digite seu email..."
                    name="email"
                    error={errors.email?.message}
                    register={register}
                />
                </div>
    
                <div className="mb-3">
                <Input
                    type="password"
                    placeholder="Digite sua senha..."
                    name="password"
                    error={errors.password?.message}
                    register={register}
                />
                </div>
    
                <button
                className="bg-zinc-900 w-full rounded-md text-white h-10 font-medium"
                type="submit"
                disabled={loadingAuth}
                >
                    {loadingAuth ? "Acessando..." : "Acessar"}
                </button>
    
            </form>

            <Link to="/register">
                Não possui uma conta? Faça o cadastro!
            </Link>
    
            </div>
        </Container>
    )
    
}