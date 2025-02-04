import logoImg from '../../assets/logoEcomerce_transparent.png'
import { Input } from '../../components/input'
import { useForm } from 'react-hook-form'
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod'
import { Container } from '../../components/container';
import { Link, useNavigate } from 'react-router-dom';
import { registerUser } from '../../services/api_cart';
import toast from 'react-hot-toast';

const schema = z.object({
    name: z.string().nonempty("O campo nome é obrigatório"),
    email: z.string().email("Insira um email válido").nonempty("O campo email é obrigatório"),
    password: z.string().min(6, "A senha deve ter pelo menos 6 caracteres").nonempty("O campo senha é obrigatório"),
    password2: z.string().nonempty("O campo confirmação de senha é obrigatório"),
    avatar: z
    .any()
        .refine((files) => files instanceof FileList && files.length > 0, {
            message: "Um arquivo é obrigatório",
        })
        .refine((files) => files instanceof FileList && files[0]?.size <= 5 * 1024 * 1024, {
            message: "O arquivo deve ter no máximo 5MB",
        })
        .optional(),
})
.refine((data) => data.password === data.password2, {
    path: ["password2"], // Foco do erro no campo password2
    message: "As senhas não correspondem",
});

type FormData = z.infer<typeof schema>

export function Register() {
    const navigate = useNavigate();
    const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
        resolver: zodResolver(schema),
        mode: "onChange"
    })

    async function onSubmit(data: FormData){
        try {
            const avatarFile = data.avatar instanceof FileList ? data.avatar[0] : null;
            const response = await registerUser({
                username: data.name,
                email: data.email,
                password: data.password,
                password2: data.password2,
                avatar: avatarFile,
            })
            console.log('Usuário cadastrado com sucesso!', response)
            toast.success("Usuário cadastrado com sucesso!")
            navigate("/login", { replace: true })
        } catch (error) {
            console.log("Erro ao cadastrar usuário")
            console.log(error)
        }
    }

    return (
        <Container>
        <div className="w-full min-h-screen flex justify-center items-center flex-col gap-4">
            <Link to="/" className="mb-6 max-w-sm w-full">
            <img
                src={logoImg}
                alt="Logo do site"
                className="w-full"
            />
            </Link>

            <form
            className="bg-white max-w-xl w-full rounded-lg p-4"
            onSubmit={handleSubmit(onSubmit)}
            >

            <div className="mb-3">
                <Input
                type="text"
                placeholder="Digite seu nome..."
                name="name"
                error={errors.name?.message}
                register={register}
                />
            </div>

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

            <div className="mb-3">
                <Input
                type="password"
                placeholder="Confirme sua senha..."
                name="password2"
                error={errors.password2?.message}
                register={register}
                />
            </div>

            <div className="mb-3">
                <label className="block text-sm font-medium text-gray-700">Avatar</label>
                <input
                    type="file"
                    accept="image/*"
                    className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    {...register("avatar")}
                />
                {typeof errors.avatar?.message === "string" && (
                    <p className="text-red-500 text-sm mt-1">{errors.avatar.message}</p>
                )}
            </div>

            <button type="submit" className="bg-zinc-900 w-full rounded-md text-white h-10 font-medium">
                Cadastrar
            </button>

            </form>

            <Link to="/login">
            Já possui uma conta? Faça o login!
            </Link>

        </div>
        </Container>
    )
}