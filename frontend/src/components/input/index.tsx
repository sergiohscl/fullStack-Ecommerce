/* eslint-disable @typescript-eslint/no-explicit-any */
import { RegisterOptions, UseFormRegister } from "react-hook-form"

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement>{
    type: string
    placeholder:string
    name: string
    register: UseFormRegister<any>
    error?: string
    rules?: RegisterOptions
}

export function Input({ name, placeholder, type, register, rules, error, ...rest }: InputProps){
    return(
        <div>
            <input
                className="w-full border-2 rounded-md h-11 px-2"
                placeholder={placeholder}
                type={type}
                {...register(name, rules)}
                id={name}
                {...rest}
            />
            {error && <p className="my-1 text-red-500">{error}</p>}
        </div>
    )
}